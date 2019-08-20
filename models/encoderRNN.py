import os
import sys

import torch
import torch.nn as nn

from models.baseRNN import BaseRNN

class EncoderRNN(BaseRNN):

    def __init__(self, vocab_size, max_len, hidden_size,
                 embedding_size, input_dropout_p=0, dropout_p=0, position_embedding=None,
                 n_layers=1, bidirectional=False, rnn_cell='lstm', variable_lengths=False,
                 embedding=None, update_embedding=True, get_context_vector=False):
        super(EncoderRNN, self).__init__(vocab_size, max_len, hidden_size,
                input_dropout_p, dropout_p, n_layers, rnn_cell)

        self.variable_lengths = variable_lengths
        self.get_context_vector = get_context_vector
        self.embedding = nn.Embedding(vocab_size, embedding_size)
        if embedding is not None:
            self.embedding.weight = nn.Parameter(embedding)
        self.pos_embedding = None
        self.position_embedding = position_embedding
        if position_embedding is not None:
            self.pos_embedding = nn.Embedding(max_len, embedding_size)
        self.embedding.weight.requires_grad = update_embedding
        self.rnn = self.rnn_cell(embedding_size, hidden_size, n_layers,
                                 batch_first=True, bidirectional=bidirectional, dropout=dropout_p)

    def length_encoding(self, batch_size, seq_len, input_lengths):
        lengths = []
        for i in range(batch_size):
            length = []
            for j in range(seq_len):
                if input_lengths[i] - j > 0:
                    length.append(input_lengths[i] - j)
                else:
                    length.append(0)
            lengths.append(length)
        return torch.tensor(lengths, device='cuda:0')

    def forward(self, input_var, input_lengths=None):
        context = None
        batch_size = input_var.size(0)
        seq_len = input_var.size(1)

        if self.get_context_vector:
            for i in range(batch_size):
                for j in range(seq_len):
                    embedded = self.embedding(input_var[i][j].unsqueeze(0).unsqueeze(0))
                    if self.position_embedding is not None:
                        lengths_tensor = self.length_encoding(batch_size, seq_len, input_lengths)
                        posemb = self.pos_embedding(lengths_tensor[i][j].unsqueeze(0).unsqueeze(0))
                        embedded = embedded + posemb

                    if j == 0:
                        output, (hx,cx) = self.rnn(embedded)
                        context = cx
                    else:
                        output_, (hx,cx) = self.rnn(embedded, (hx,cx))
                        output = torch.cat((output, output_), dim=1)
                        context = torch.cat((context, cx), dim=1)
            hidden = (hx,cx)
        else:
            embedded = self.embedding(input_var)
            if self.position_embedding is not None:
                posemb = self.pos_embedding(self.length_encoding(batch_size, seq_len, input_lengths))
                embedded = embedded + posemb
            #embedded = self.input_dropout(embedded)

            if self.variable_lengths:
                embedded = nn.utils.rnn.pack_padded_sequence(embedded, input_lengths, batch_first=True)
            output, hidden = self.rnn(embedded)
            if self.variable_lengths:
                output, _ = nn.utils.rnn.pad_packed_sequence(output, batch_first=True)

        return output, hidden, context
