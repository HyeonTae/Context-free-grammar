from __future__ import division
import logging
import os
import random
import time

import torch
import torchtext
from torch import optim

from evaluator.evaluator import Evaluator
from loss.loss import NLLLoss
from optim.optim import Optimizer

import matplotlib.pyplot as plt

class Trainer(object):
    def __init__(self, loss=NLLLoss(), batch_size=64,
                 random_seed=None,
                 checkpoint_every=100, print_every=100, hidden_size=50, path="test", file_name="test"):
        self.hidden_size = hidden_size
        self.fig_path = "log/plot/" + path + "/" + file_name
        self.check_path = "log/check_point/" + path + "/" + file_name
        self.torch_save_path = "log/pth/" + path + "_" + file_name
        self._trainer = "Simple Trainer"
        self.random_seed = random_seed
        if random_seed is not None:
            random.seed(random_seed)
            torch.manual_seed(random_seed)
        self.loss = loss
        self.evaluator = Evaluator(loss=self.loss, batch_size=batch_size)
        self.optimizer = None
        self.checkpoint_every = checkpoint_every
        self.print_every = print_every

        if not os.path.isdir("log/plot/" + path):
            os.mkdir("log/plot/" + path)
        if not os.path.isdir("log/check_point/" + path):
            os.mkdir("log/check_point/" + path)

        self.batch_size = batch_size

        self.logger = logging.getLogger(__name__)

    def _train_batch(self, input_variable, input_lengths, target_variable, target_lengths, model, teacher_forcing_ratio):
        loss = self.loss
        # Forward propagation
        decoder_outputs, decoder_hidden, other = model(input_variable, input_lengths, target_variable,
                                                       target_lengths, teacher_forcing_ratio=teacher_forcing_ratio)
        # Get loss
        loss.reset()
        for step, step_output in enumerate(decoder_outputs):
            batch_size = target_variable.size(0)
            loss.eval_batch(step_output.contiguous().view(batch_size, -1), target_variable[:, step + 1])
        # Backward propagation
        model.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.get_loss()

    def _train_epoches(self, data, model, n_epochs, start_epoch, start_step,
                       dev_data=None, teacher_forcing_ratio=0):
        log = self.logger

        print_loss_total = 0  # Reset every print_every
        epoch_loss_total = 0  # Reset every epoch

        #device = torch.cuda if torch.cuda.is_available() else torch
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        batch_iterator = torchtext.data.BucketIterator(
            dataset=data, batch_size=self.batch_size,
            sort=False, sort_within_batch=True,
            sort_key=lambda x: len(x.src),
            device=device, repeat=False)

        steps_per_epoch = len(batch_iterator)
        total_steps = steps_per_epoch * n_epochs

        step = start_step
        step_elapsed = 0
        epoch_list = []
        losses = []
        character_accuracy_list = []
        sentence_accuracy_list = []
        f1_score_list = []
        best_character_accuracy = 0
        best_sentence_accuracy = 0
        best_f1_score = 0
        for epoch in range(start_epoch, n_epochs + 1):
            epoch_list.append(epoch)
            log.debug("Epoch: %d, Step: %d" % (epoch, step))

            batch_generator = batch_iterator.__iter__()
            # consuming seen batches from previous training
            for _ in range((epoch - 1) * steps_per_epoch, step):
                next(batch_generator)

            model.train(True)
            for batch in batch_generator:
                step += 1
                step_elapsed += 1

                input_variables, input_lengths = getattr(batch, 'src')
                target_variables, target_lengths = getattr(batch, 'tgt')

                loss = self._train_batch(input_variables, input_lengths.tolist(), target_variables, target_lengths.tolist(), model, teacher_forcing_ratio)

                # Record average loss
                print_loss_total += loss
                epoch_loss_total += loss

                if step % self.print_every == 0 and step_elapsed > self.print_every:
                    print_loss_avg = print_loss_total / self.print_every
                    print_loss_total = 0
                    log_msg = 'Progress: %d%%, Train %s: %.4f' % (
                        step / total_steps * 100,
                        self.loss.name,
                        print_loss_avg)
                    # Print learning check
                    #log.info(log_msg)

                # Checkpoint
                """
                if step % self.checkpoint_every == 0 or step == total_steps:
                    Checkpoint(model=model,
                               optimizer=self.optimizer,
                               epoch=epoch, step=step,
                               input_vocab=data.fields['src'].vocab,
                               output_vocab=data.fields['tgt'].vocab).save(self.expt_dir)
                """

            if step_elapsed == 0: continue

            epoch_loss_avg = epoch_loss_total / min(steps_per_epoch, step - start_step)
            epoch_loss_total = 0
            log_msg = "Finished epoch %d: Train %s: %.4f" % (epoch, self.loss.name, epoch_loss_avg)
            losses.append(epoch_loss_avg)
            if dev_data is not None:
                dev_loss, character_accuracy, sentence_accuracy, f1_score = self.evaluator.evaluate(model, dev_data)
                self.optimizer.update(dev_loss, epoch)
                log_msg += ", Dev %s: %.4f, Accuracy(character): %.4f, Accuracy(sentence): %.4f, F1 Score: %.4f" % (self.loss.name, dev_loss, character_accuracy, sentence_accuracy, f1_score)
                model.train(mode=True)
            else:
                self.optimizer.update(epoch_loss_avg, epoch)

            character_accuracy_list.append(character_accuracy)
            sentence_accuracy_list.append(sentence_accuracy)
            f1_score_list.append(f1_score)
            log.info(log_msg)

            if best_character_accuracy < character_accuracy:
                best_character_accuracy = character_accuracy
            if best_sentence_accuracy < sentence_accuracy:
                best_sentence_accuracy = sentence_accuracy
            if best_f1_score < f1_score:
                torch_save = self.torch_save_path + "_model_save.pth"
                torch.save(model.state_dict(), torch_save)
                best_f1_score = f1_score

            if not os.path.isdir(self.check_path):
                os.mkdir(self.check_path)

            with open(self.check_path + "/epoch" + str(epoch), 'w') as f:
                f.write("Train Loss:%0.4f, Dev Loss:%0.4f, Best Character Accuracy:%0.4f, Best Sentence Accuracy:%0.4f, Best F1 Score:%0.4f" % (epoch_loss_avg, dev_loss, best_character_accuracy, best_sentence_accuracy, best_f1_score))

        if not os.path.isdir(self.fig_path):
            os.mkdir(self.fig_path)

        plt.figure(figsize=(15,10))
        plt.grid(True)
        title = "epoch_to_loss" + str(self.hidden_size)
        save_path = self.fig_path + "/" + title
        plt.plot(epoch_list[::3], losses[::3], LineWidth=4)
        plt.xlabel('epoch', fontsize=24)
        plt.ylabel('loss', fontsize=24)
        plt.title(title, fontsize=32, fontweight=560)
        plt.savefig(save_path + '.png')

        plt.figure(figsize=(15,10))
        plt.grid(True)
        title = "epoch_to_character_accuracy_" + str(self.hidden_size)
        save_path = self.fig_path + "/" + title
        plt.plot(epoch_list[::3], character_accuracy_list[::3], LineWidth=4)
        plt.xlabel('epoch', fontsize=24)
        plt.ylabel('character accuracy', fontsize=24)
        plt.title(title, fontsize=32, fontweight=560)
        plt.savefig(save_path + '.png')

        plt.figure(figsize=(15,10))
        plt.grid(True)
        title = "epoch_to_sentence_accuracy_" + str(self.hidden_size)
        save_path = self.fig_path + "/" + title
        plt.plot(epoch_list[::3], sentence_accuracy_list[::3], LineWidth=4)
        plt.xlabel('epoch', fontsize=24)
        plt.ylabel('sentence accuracy', fontsize=24)
        plt.title(title, fontsize=32, fontweight=560)
        plt.savefig(save_path + '.png')

        plt.figure(figsize=(15,10))
        plt.grid(True)
        title = "epoch_to_f1_score_" + str(self.hidden_size)
        save_path = self.fig_path + "/" + title
        plt.plot(epoch_list[::3], f1_score_list[::3], LineWidth=4)
        plt.xlabel('epoch', fontsize=24)
        plt.ylabel('f1_score', fontsize=24)
        plt.title(title, fontsize=32, fontweight=560)
        plt.savefig(save_path + '.png')

        #plt.plot(epoch_list, losses)
        #plt.savefig('epoch_to_loss.png')
        return epoch_loss_avg, character_accuracy_list, sentence_accuracy_list, f1_score_list

    def train(self, model, data, num_epochs=5,
              resume=False, dev_data=None,
              optimizer=None, teacher_forcing_ratio=0):
        # If training is set to resume
        """
        if resume:
            latest_checkpoint_path = Checkpoint.get_latest_checkpoint(self.expt_dir)
            resume_checkpoint = Checkpoint.load(latest_checkpoint_path)
            model = resume_checkpoint.model
            self.optimizer = resume_checkpoint.optimizer

            # A walk around to set optimizing parameters properly
            resume_optim = self.optimizer.optimizer
            defaults = resume_optim.param_groups[0]
            defaults.pop('params', None)
            defaults.pop('initial_lr', None)
            self.optimizer.optimizer = resume_optim.__class__(model.parameters(), **defaults)

            start_epoch = resume_checkpoint.epoch
            step = resume_checkpoint.step
        """
        #else:
        start_epoch = 1
        step = 0
        if optimizer is "Adam":
            optimizer = Optimizer(optim.Adam(model.parameters()), max_grad_norm=0.5)
        self.optimizer = optimizer

        self.logger.info("Optimizer: %s, Scheduler: %s" % (self.optimizer.optimizer, self.optimizer.scheduler))

        loss, character_accuracy, sentence_accuracy, f1_score = self._train_epoches(data, model, num_epochs,
                                    start_epoch, step, dev_data=dev_data,
                                    teacher_forcing_ratio=teacher_forcing_ratio)
        return model, loss, character_accuracy, sentence_accuracy, f1_score
