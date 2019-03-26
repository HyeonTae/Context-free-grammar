#!/bin/bash

echo `shuf grammar_data.txt -o grammar_data_shuf.txt`
echo `split -l 5000 grammar_data_shuf.txt`
echo `mv xaa data_train.txt`
echo `mv xab data_test.txt`
