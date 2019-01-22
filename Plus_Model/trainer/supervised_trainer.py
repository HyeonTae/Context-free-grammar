from __future__ import division
import logging
import os
import random
import time
<<<<<<< HEAD
=======
#import sys
>>>>>>> d6b28b16f2d9d234eed996c477a5c4f7a9d53268

import torch
import torchtext
from torch import optim

<<<<<<< HEAD
from evaluator.evaluator import Evaluator
from loss.loss import NLLLoss
from optim.optim import Optimizer

import matplotlib.pyplot as plt
=======
#sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from evaluator.evaluator import Evaluator
from loss.loss import NLLLoss
from optim.optim import Optimizer
#from util.checkpoint import Checkpoint
>>>>>>> d6b28b16f2d9d234eed996c477a5c4f7a9d53268

class SupervisedTrainer(object):
    def __init__(self, loss=NLLLoss(), batch_size=64,
                 random_seed=None,
                 checkpoint_every=100, print_every=100):
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

        #if not os.path.isabs(expt_dir):
        #    expt_dir = os.path.join(os.getcwd(), expt_dir)
        #self.expt_dir = expt_dir
        #if not os.path.exists(self.expt_dir):
        #    os.makedirs(self.expt_dir)
        self.batch_size = batch_size

        self.logger = logging.getLogger(__name__)

    def _train_batch(self, input_variable, input_lengths, target_variable, model, teacher_forcing_ratio):
        loss = self.loss
        # Forward propagation
        decoder_outputs, decoder_hidden, other = model(input_variable, input_lengths, target_variable,
                                                       teacher_forcing_ratio=teacher_forcing_ratio)
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
<<<<<<< HEAD
        epoch_list = []
        losses = []
        for epoch in range(start_epoch, n_epochs + 1):
            epoch_list.append(epoch)
=======
        for epoch in range(start_epoch, n_epochs + 1):
>>>>>>> d6b28b16f2d9d234eed996c477a5c4f7a9d53268
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
                target_variables = getattr(batch, 'tgt')

                loss = self._train_batch(input_variables, input_lengths.tolist(), target_variables, model, teacher_forcing_ratio)

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
<<<<<<< HEAD
                    # Print learning check
                    #log.info(log_msg)
=======
                    log.info(log_msg)
>>>>>>> d6b28b16f2d9d234eed996c477a5c4f7a9d53268

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
<<<<<<< HEAD
            losses.append(epoch_loss_avg)
=======
>>>>>>> d6b28b16f2d9d234eed996c477a5c4f7a9d53268
            if dev_data is not None:
                dev_loss, character_accuracy, word_accuracy = self.evaluator.evaluate(model, dev_data)
                self.optimizer.update(dev_loss, epoch)
                log_msg += ", Dev %s: %.4f, Accuracy(Character): %.4f, Accuracy(Word): %.4f" % (self.loss.name, dev_loss, character_accuracy, word_accuracy)
                model.train(mode=True)
            else:
                self.optimizer.update(epoch_loss_avg, epoch)

            log.info(log_msg)

<<<<<<< HEAD
        plt.plot(epoch_list, losses)
        plt.savefig('epoch_to_loss.png')
=======
>>>>>>> d6b28b16f2d9d234eed996c477a5c4f7a9d53268
        return epoch_loss_avg, character_accuracy

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
<<<<<<< HEAD
        if optimizer is "Adam":
            optimizer = Optimizer(optim.Adam(model.parameters()), max_grad_norm=0.5)
=======
        if optimizer is None:
            optimizer = Optimizer(optim.Adam(model.parameters()), max_grad_norm=5)
>>>>>>> d6b28b16f2d9d234eed996c477a5c4f7a9d53268
        self.optimizer = optimizer

        self.logger.info("Optimizer: %s, Scheduler: %s" % (self.optimizer.optimizer, self.optimizer.scheduler))

        loss, character_accuracy = self._train_epoches(data, model, num_epochs,
                                    start_epoch, step, dev_data=dev_data,
                                    teacher_forcing_ratio=teacher_forcing_ratio)
        return model, loss, character_accuracy
