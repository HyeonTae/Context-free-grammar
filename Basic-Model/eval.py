from __future__ import unicode_literals, print_function, division
from io import open
import unicodedata
import string
import re
import random

import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

SOS_token = 0
EOS_token = 1

class Grammar:
    def __init__(self, name):
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {0: "SOS", 1: "EOS"}
        self.n_words = 2

    def addSentence_bracket(self, sentence):
        for bracket in sentence:
            self.addWord(bracket)

    def addSentence_depth(self, sentence):
        for depth in sentence.split(','):
            self.addWord(depth)

    def addWord(self, word):
        if(word not in self.word2index):
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1

def readGrammars(bracket, depth):
    print("Reading lines...")
    lines = open('data/grammar_data.txt').read().strip().split('\n')
    pairs = [[s for s in l.split('\t')] for l in lines]
    input_bracket = Grammar(bracket)
    output_depth = Grammar(depth)

    return input_bracket, output_depth, pairs

def prepareData(bracket, depth):
    input_bracket, output_depth, pairs = readGrammars(bracket, depth)
    print("Read %s sentence pairs" % len(pairs))
    print("Counting brackets...")
    for pair in pairs:
        input_bracket.addSentence_bracket(pair[0])
        output_depth.addSentence_depth(pair[1])
    print("Counted brackets:")
    print(input_bracket.name, input_bracket.n_words)
    print(output_depth.name, output_depth.n_words)
    return input_bracket, output_depth, pairs

input_bracket, output_depth, pairs = prepareData('grammar', 'depth')

def indexesFromSentence_bracket(grammar, sentence):
    return [grammar.word2index[word] for word in sentence]

def indexesFromSentence_depth(grammar, sentence):
    return [grammar.word2index[word] for word in sentence.split(',')]


def tensorFromSentence_bracket(grammar, sentence):
    indexes = indexesFromSentence_bracket(grammar, sentence)
    indexes.append(EOS_token)
    return torch.tensor(indexes, dtype=torch.long, device=device).view(-1, 1)

def tensorFromSentence_depth(grammar, sentence):
    indexes = indexesFromSentence_depth(grammar, sentence)
    indexes.append(EOS_token)
    return torch.tensor(indexes, dtype=torch.long, device=device).view(-1, 1)

def tensorsFromPair(pair):
    input_tensor = tensorFromSentence_bracket(input_bracket, pair[0])
    target_tensor = tensorFromSentence_depth(output_depth, pair[1])
    return (input_tensor, target_tensor)

def normalizeString(s):
    s = re.sub("[a-zA-Z0-9""'',.?!/~%:=&|^$#@+*()-]", "", s)
    s = s.replace(" ","")
    return s

MAX_LENGTH = 101

class EncoderRNN(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(EncoderRNN, self).__init__()
        self.hidden_size = hidden_size

        self.embedding = nn.Embedding(input_size, hidden_size)
        #self.lstm = nn.GRU(hidden_size, hidden_size)
        self.lstm = nn.LSTM(hidden_size, hidden_size)

    def forward(self, input, hidden):
        embedded = self.embedding(input).view(1, 1, -1)
        output = embedded
        output, hidden = self.lstm(output, hidden)
        return output, hidden

    def initHidden(self):
        return (torch.zeros(1, 1, self.hidden_size, device=device),
                torch.zeros(1, 1, self.hidden_size, device=device))

class DecoderRNN(nn.Module):
    def __init__(self, hidden_size, output_size):
        super(DecoderRNN, self).__init__()
        self.hidden_size = hidden_size

        self.embedding = nn.Embedding(output_size, hidden_size)
        #self.lstm = nn.GRU(hidden_size, hidden_size)
        self.lstm = nn.LSTM(hidden_size, hidden_size)
        self.out = nn.Linear(hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, input, hidden):
        output = self.embedding(input).view(1, 1, -1)
        output = F.relu(output)
        output, hidden = self.lstm(output, hidden)
        output = self.softmax(self.out(output[0]))
        return output, hidden

    def initHidden(self):
        return (torch.zeros(1, 1, self.hidden_size, device=device),
                torch.zeros(1, 1, self.hidden_size, device=device))

def evaluate(encoder, decoder, sentence, max_length=MAX_LENGTH):
    with torch.no_grad():
        input_tensor = tensorFromSentence_bracket(input_bracket, sentence)
        input_length = input_tensor.size()[0]
        encoder_hidden = encoder.initHidden()

        #encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)

        for ei in range(input_length):
            encoder_output, encoder_hidden = encoder(input_tensor[ei], encoder_hidden)
            #encoder_outputs[ei] = encoder_outputs[ei] + encoder_output[0][0]

        decoder_input = torch.tensor([[SOS_token]], device=device)

        decoder_hidden = encoder_hidden

        decoded_words = []

        for di in range(max_length):
            decoder_output, decoder_hidden = decoder(decoder_input, decoder_hidden)
            topv, topi = decoder_output.data.topk(1)
            if topi.item() == EOS_token:
                decoded_words.append('<EOS>')
                break
            else:
                decoded_words.append(output_depth.index2word[topi.item()])

            decoder_input = topi.squeeze().detach()

        return decoded_words

def evaluateRandomly(encoder, decoder, n=5):
    print("-------------------in-sample-------------------")
    for i in range(n):
        pair = random.choice(pairs)
        print(">", pair[0])
        print("=", pair[1])
        output_words = evaluate(encoder, decoder, pair[0])
        output_sentence = ",".join(output_words)
        print("<",output_sentence)
        print("")

    print("-----------------out-of-sample-----------------")
    while(True):
        stack = []
        stack_size = []
        s = input("input(exit=q) : ")
        if(s == "q"):
            break

        print(">", s)
        bracket = normalizeString(s)
        for i in bracket:
            if(i == "{" or i == "["):
                stack.append(i)
                stack_size.append(str(len(stack)))
            elif(i == "}" or i == "]"):
                stack.pop()
                stack_size.append(str(len(stack)))

        print("=", ",".join(stack_size))
        output_words = evaluate(encoder, decoder, bracket)
        output_sentence = ",".join(output_words)
        print("<",output_sentence)
        print("")

hidden_size = 50

encoder = EncoderRNN(input_bracket.n_words, hidden_size).to(device)
encoder.load_state_dict(torch.load('log/encoder.pth'))
encoder.eval()
decoder = DecoderRNN(hidden_size, output_depth.n_words).to(device)
decoder.load_state_dict(torch.load('log/decoder.pth'))
decoder.eval()

evaluateRandomly(encoder, decoder)
