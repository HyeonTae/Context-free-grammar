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
        self.bracket2index = {}
        self.bracket2count = {}
        self.index2bracket = {0: "SOS", 1: "EOS"}
        self.n_brackets = 2

    def addSentence_bracket(self, sentence):
        for bracket in sentence:
            self.addBracket(bracket)

    def addSentence_depth(self, sentence):
        for bracket in sentence.split(','):
            self.addBracket(bracket)

    def addBracket(self, bracket):
        if(bracket not in self.bracket2index):
            self.bracket2index[bracket] = self.n_brackets
            self.bracket2count[bracket] = 1
            self.index2bracket[self.n_brackets] = bracket
            self.n_brackets += 1
        else:
            self.bracket2count[bracket] += 1

def readGrammars(grammar, depth):
    print("Reading lines...")
    lines = open('ooo.txt').read().strip().split('\n')
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
    print(input_grammar.name, input_grammar.n_brackets)
    print(output_depth.name, output_depth.n_brackets)
    return input_grammar, output_depth, pairs

input_grammar, output_depth, pairs = prepareData('grammar', 'depth')
print(random.choice(pairs))
