## Evaluating the Ability of LSTMs to Learn Context-Free Grammars

We are trying to reproduce the results of the paper 'Evaluating the Ability of LSTMs to Learn Context-Free Grammars' presented at ACL 2018.


## Future plan

    1. Construct a corpus with the same statistics with that used in the paper.
    2. Train a vanilla sequence-to-sequence model to reproduce the behaviour observed in the paper.
    3. Extend the result by trying out different models for machine translation.

## To-do
 - [ ] Modify the distance function
 - [X] Compare performances of various sequence-to-sequence vanilla seq2seq models
 - [ ] Compare performances of various sequence-to-sequence attentional models
 - [ ] Generate random strings with non-bracket characters such as a,b, and c.
 - [ ] Generate random strings with unmatching brackets (e.g. '[[}]', '{]')
 
## Memo
Please check the "Plus_Model/train_units_to_error_rate_and_accuracy.ipynb" file.
