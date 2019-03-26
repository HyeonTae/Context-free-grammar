from __future__ import print_function, division

import os
import torch
import torchtext
import itertools

from loss.loss import NLLLoss

class Evaluator(object):
    def __init__(self, loss=NLLLoss(), batch_size=64):
        self.loss = loss
        self.batch_size = batch_size

    def evaluate(self, model, data):
        model.eval()

        loss = self.loss
        loss.reset()
        match = 0
        total = 0

        match_sentance = 0
        total_lengths = 0

        #device = None if torch.cuda.is_available() else -1
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        batch_iterator = torchtext.data.BucketIterator(
            dataset=data, batch_size=self.batch_size,
            sort=True, sort_key=lambda x: len(x.src),
            device=device, train=False)
        tgt_vocab = data.fields['tgt'].vocab
        pad = tgt_vocab.stoi[data.fields['tgt'].pad_token]

        with torch.no_grad():
            for batch in batch_iterator:
                input_variables, input_lengths  = getattr(batch, 'src')
                target_variables = getattr(batch, 'tgt')

                decoder_outputs, decoder_hidden, other = model(input_variables, input_lengths.tolist(), target_variables)
                correct_list = []
                # Evaluation
                seqlist = other['sequence']
                for step, step_output in enumerate(decoder_outputs):
                    target = target_variables[:, step + 1]
                    loss.eval_batch(step_output.view(target_variables.size(0), -1), target)

                    non_padding = target.ne(pad)
                    correct = seqlist[step].view(-1).eq(target).masked_select(non_padding).sum().item()
                    correct_list.append(seqlist[step].view(-1).eq(target).masked_select(non_padding).tolist())
                    match += correct
                    total += non_padding.sum().item()

                q = list(itertools.zip_longest(*correct_list))
                for i in q:
                    check_sentance = False
                    for j in i:
                        if(j == 0):
                            check_sentance = True
                    if(check_sentance == False):
                        match_sentance += 1
                total_lengths += len(input_lengths)

        if total == 0:
            character_accuracy = float('nan')
            sentance_accuracy = float('nan')
        else:
            character_accuracy = match / total
            sentance_accuracy = match_sentance / total_lengths

        return loss.get_loss(), character_accuracy, sentance_accuracy
