import os
import sys
import random

import numpy as np

import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F

from models.attention import Attention
from models.hard_attention import HardAttention
from models.baseRNN import BaseRNN

if torch.cuda.is_available():
    import torch.cuda as device
else:
    import torch as device

class DecoderRNN(BaseRNN):
    KEY_ATTN_SCORE = 'attention_score'
    KEY_LENGTH = 'length'
    KEY_SEQUENCE = 'sequence'
    KEY_ENCODER_OUTPUTS = 'encoder_outputs'
    KEY_ENCODER_CONTEXT = 'encoder_context'

    def __init__(self, vocab_size, max_len, hidden_size, embedding_size,
            sos_id, eos_id, input_dropout_p=0, dropout_p=0, position_embedding=None,
            n_layers=1, bidirectional=False, rnn_cell='lstm',use_attention=True,
            attn_layers=1, hard_attn=False):
        super(DecoderRNN, self).__init__(vocab_size, max_len, hidden_size,
                input_dropout_p, dropout_p,
                n_layers, rnn_cell)

        self.bidirectional_encoder = bidirectional

        self.output_size = vocab_size
        self.attn_layers = attn_layers
        self.max_length = max_len
        self.use_attention = use_attention
        self.hard_attn = hard_attn
        self.eos_id = eos_id
        self.sos_id = sos_id

        self.init_input = None

        self.embedding = nn.Embedding(self.output_size, embedding_size)
        self.position_embedding = position_embedding
        self.pos_embedding = None
        if position_embedding is not None:
            self.pos_embedding = nn.Embedding(max_len, embedding_size)

        self.rnn = self.rnn_cell(embedding_size, hidden_size, n_layers, batch_first=True, dropout=dropout_p)
        if use_attention:
            if hard_attn:
                self.attention = Attention(self.hidden_size)
                self.hard_attention = HardAttention(self.hidden_size)
                self.out = nn.Linear(self.hidden_size*2, self.output_size)
            else:
                if attn_layers is 1:
                    self.attention1 = Attention(self.hidden_size)
                    self.out = nn.Linear(self.hidden_size, self.output_size)
                elif attn_layers is 2:
                    self.attention1 = Attention(self.hidden_size)
                    self.attention2 = Attention(self.hidden_size)
                    self.out = nn.Linear(self.hidden_size*2, self.output_size)
                elif attn_layers is 3:
                    self.attention1 = Attention(self.hidden_size)
                    self.attention2 = Attention(self.hidden_size)
                    self.attention3 = Attention(self.hidden_size)
                    self.out = nn.Linear(self.hidden_size*3, self.output_size)
        else:
            self.out = nn.Linear(self.hidden_size, self.output_size)

    def forward_step(self, input_var, input_length, hidden, encoder_outputs, di, function):
        batch_size = input_var.size(0)
        output_size = input_var.size(1)
        
        embedded = self.embedding(input_var)
        if input_length is not None:
            posemb = self.pos_embedding(input_length)
            embedded = embedded + posemb
        output, hidden = self.rnn(embedded, hidden)

        attn = None
        if self.use_attention:
            if self.hard_attn:
                s_output, s_attn = self.attention(output, encoder_outputs)
                h_output, h_attn = self.hard_attention(output, encoder_outputs, di)
                output = torch.cat((s_output, h_output), dim=2)
                attn = torch.cat((s_attn, h_attn), dim=1)
                hidden_sizes = self.hidden_size*2
            else:
                if self.attn_layers is 1:
                    output, attn = self.attention1(output, encoder_outputs)
                    hidden_sizes = self.hidden_size
                elif self.attn_layers is 2:
                    output1, attn1 = self.attention1(output, encoder_outputs)
                    output2, attn2 = self.attention2(output, encoder_outputs)
                    output = torch.cat((output1, output2), dim=2)
                    attn = torch.cat((attn1, attn2), dim=1)
                    hidden_sizes = self.hidden_size*2
                elif self.attn_layers is 3:
                    output1, attn1 = self.attention1(output, encoder_outputs)
                    output2, attn2 = self.attention2(output, encoder_outputs)
                    output3, attn3 = self.attention3(output, encoder_outputs)
                    output = torch.cat((output1, output2, output3), dim=2)
                    attn = torch.cat((attn1, attn2, attn3), dim=1)
                    hidden_sizes = self.hidden_size*3
        else:
            hidden_sizes = self.hidden_size

        predicted_softmax = function(self.out(output.contiguous().view(-1, hidden_sizes)), dim=1).view(batch_size, output_size, -1)
        return predicted_softmax, hidden, attn

    def length_encoding(self, batch_size, seq_len, max_length, inputs_lengths):
        result = []
        if seq_len != 0:
            for i in range(batch_size):
                length = []
                for j in range(seq_len):
                    if j == 0 or inputs_lengths[i]-1 - j <= 0:
                        length.append(0)
                    else:
                        length.append(inputs_lengths[i]-1 - j)
                result.append(length)
        else:
            for i in range(batch_size):
                length = []
                for j in range(max_length):
                    if j == 0 or inputs_lengths[i]-1 - j <= 0:
                        length.append(0)
                    else:
                        length.append(inputs_lengths[i]-1 - j)
                result.append(length)
        return result

    def forward(self, inputs=None, inputs_lengths=None, encoder_hidden=None, encoder_outputs=None,
                    encoder_context=None, function=F.log_softmax, teacher_forcing_ratio=0):
        ret_dict = dict()
        ret_dict[DecoderRNN.KEY_ENCODER_OUTPUTS] = encoder_outputs.squeeze(0)
        if encoder_context is not None:
            ret_dict[DecoderRNN.KEY_ENCODER_CONTEXT] = encoder_context.squeeze(0)
        else:
            ret_dict[DecoderRNN.KEY_ENCODER_CONTEXT] = None

        if self.use_attention:
            ret_dict[DecoderRNN.KEY_ATTN_SCORE] = list()

        # input.shape = batch_size x sequence_length
        # encoder_outputs.shape = batch_size x sequence_length (50) x hidden_size (50 x 2)
        # encoder_hidden = tuple of the last hidden state and the last cell state.
        # Last cell state = number of layers * batch_size * hidden_size
        # Last hidden state = the same as above

        inputs, batch_size, max_length = self._validate_args(inputs, encoder_hidden, encoder_outputs,
                                                             function, teacher_forcing_ratio)
        decoder_hidden = self._init_state(encoder_hidden)

        use_teacher_forcing = True if random.random() < teacher_forcing_ratio else False

        decoder_outputs = []
        sequence_symbols = []
        lengths = np.array([max_length] * batch_size)

        def decode(step, step_output, step_attn):
            decoder_outputs.append(step_output)
            if self.use_attention:
                ret_dict[DecoderRNN.KEY_ATTN_SCORE].append(step_attn)
            symbols = decoder_outputs[-1].topk(1)[1]
            sequence_symbols.append(symbols)

            eos_batches = symbols.data.eq(self.eos_id)
            if eos_batches.dim() > 0:
                eos_batches = eos_batches.cpu().view(-1).numpy()
                update_idx = ((lengths > step) & eos_batches) != 0
                lengths[update_idx] = len(sequence_symbols)
            return symbols

        length_tensor = None
        if use_teacher_forcing:
            if self.position_embedding is not None:
                len_encod = self.length_encoding(inputs.size(0), inputs.size(1)-1, max_length, inputs_lengths)
                length_tensor = torch.tensor(len_encod, device='cuda:0')

            decoder_input = inputs[:, :-1]
            decoder_output, decoder_hidden, attn = self.forward_step(decoder_input, length_tensor, decoder_hidden, encoder_outputs, di=0, function=function)

            for di in range(decoder_output.size(1)):
                step_output = decoder_output[:, di, :]
                if attn is not None:
                    step_attn = attn[:, di, :]
                else:
                    step_attn = None
                decode(di, step_output, step_attn)
        else:
            decoder_input = inputs[:, 0].unsqueeze(1)
            for di in range(max_length):
                if self.position_embedding is not None:
                    decoder_input_length = []
                    len_encod = self.length_encoding(inputs.size(0), inputs.size(1)-1, max_length, inputs_lengths)
                    for i in range(len(len_encod)):
                        decoder_input_length.append([len_encod[i][di]])
                    length_tensor = torch.tensor(decoder_input_length, device='cuda:0')

                decoder_output, decoder_hidden, step_attn = self.forward_step(decoder_input, length_tensor, decoder_hidden, encoder_outputs, di, function=function)
                step_output = decoder_output.squeeze(1)
                symbols = decode(di, step_output, step_attn)
                decoder_input = symbols

        ret_dict[DecoderRNN.KEY_SEQUENCE] = sequence_symbols
        ret_dict[DecoderRNN.KEY_LENGTH] = lengths.tolist()

        return decoder_outputs, decoder_hidden, ret_dict

    def _init_state(self, encoder_hidden):
        if encoder_hidden is None:
            return None
        if isinstance(encoder_hidden, tuple):
            encoder_hidden = tuple([self._cat_directions(h) for h in encoder_hidden])
        else:
            encoder_hidden = self._cat_directions(encoder_hidden)
        return encoder_hidden

    def _cat_directions(self, h):
        if self.bidirectional_encoder:
            h = torch.cat([h[0:h.size(0):2], h[1:h.size(0):2]], 2)
        return h

    def _validate_args(self, inputs, encoder_hidden, encoder_outputs, function, teacher_forcing_ratio):
        if self.use_attention:
            if encoder_outputs is None:
                raise ValueError("Argument encoder_outputs cannot be None when attention is used.")

        # inference batch size
        if inputs is None and encoder_hidden is None:
            batch_size = 1
        else:
            if inputs is not None:
                batch_size = inputs.size(0)
            else:
                if self.rnn_cell is nn.LSTM:
                    batch_size = encoder_hidden[0].size(1)
                elif self.rnn_cell is nn.GRU:
                    batch_size = encoder_hidden.size(1)

        # set default input and max decoding length
        if inputs is None:
            if teacher_forcing_ratio > 0:
                raise ValueError("Teacher forcing has to be disabled (set 0) when no inputs is provided.")
            inputs = torch.LongTensor([self.sos_id] * batch_size).view(batch_size, 1)
            if torch.cuda.is_available():
                inputs = inputs.cuda()
            max_length = self.max_length
        else:
            max_length = inputs.size(1) - 1 # minus the start of sequence symbol

        return inputs, batch_size, max_length
