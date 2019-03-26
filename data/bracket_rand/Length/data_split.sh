#!/bin/bash

echo `shuf -o grammar_data_N60_shuf.txt grammar_data_N60.txt`
echo `split -l 5000 grammar_data_N60_shuf.txt`
echo `mv xaa N60_data_train.txt`
echo `mv xab N60_data_test.txt`

echo `shuf -o grammar_data_N80_shuf.txt grammar_data_N80.txt`
echo `split -l 5000 grammar_data_N80_shuf.txt`
echo `mv xaa N80_data_train.txt`
echo `mv xab N80_data_test.txt`

echo `shuf -o grammar_data_N100_shuf.txt grammar_data_N100.txt`
echo `split -l 5000 grammar_data_N100_shuf.txt`
echo `mv xaa N100_data_train.txt`
echo `mv xab N100_data_test.txt`

echo `shuf -o grammar_data_N120_shuf.txt grammar_data_N120.txt`
echo `split -l 5000 grammar_data_N120_shuf.txt`
echo `mv xaa N120_data_train.txt`
echo `mv xab N120_data_test.txt`

echo `shuf -o grammar_data_N140_shuf.txt grammar_data_N140.txt`
echo `split -l 5000 grammar_data_N140_shuf.txt`
echo `mv xaa N140_data_train.txt`
echo `mv xab N140_data_test.txt`

echo `shuf -o grammar_data_N160_shuf.txt grammar_data_N160.txt`
echo `split -l 5000 grammar_data_N160_shuf.txt`
echo `mv xaa N160_data_train.txt`
echo `mv xab N160_data_test.txt`

echo `shuf -o grammar_data_N180_shuf.txt grammar_data_N180.txt`
echo `split -l 5000 grammar_data_N180_shuf.txt`
echo `mv xaa N180_data_train.txt`
echo `mv xab N180_data_test.txt`

echo `shuf -o grammar_data_N200_shuf.txt grammar_data_N200.txt`
echo `split -l 5000 grammar_data_N200_shuf.txt`
echo `mv xaa N200_data_train.txt`
echo `mv xab N200_data_test.txt`
