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

def readGrammars(grammar, depth):
    print("Reading lines...")
    lines = open('grammar_data.txt').read().strip().split('\n')
    pairs = [[s for s in l.split('\t')] for l in lines]
    input_grammar = Grammar(grammar)
    output_depth = Grammar(depth)

    return input_grammar, output_depth, pairs

def prepareData(grammar, depth):
    input_grammar, output_depth, pairs = readGrammars(grammar, depth)
    print("Read %s sentence pairs" % len(pairs))
    print("Counting brackets...")
    for pair in pairs:
        input_grammar.addSentence_bracket(pair[0])
        output_depth.addSentence_depth(pair[1])
    print("Counted brackets:")
    print(input_grammar.name, input_grammar.n_words)
    print(output_depth.name, output_depth.n_words)
    return input_grammar, output_depth, pairs

input_grammar, output_depth, pairs = prepareData('grammar', 'depth')
print(random.choice(pairs))
