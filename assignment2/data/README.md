# wv-da
Word Vector Domain Adapation

dataset - contains the training data
eval_data.txt - the evaluation data
eval_data.txt.td - target dictionary for the evaluation data

mrr.py - Computes the mrr metric
Run it using,
python mrr.py eval_data.txt eval_data.txt.td output.txt

where each line of output.txt contains a space-separated list of ranks for each word in the  corresponding line of the target dictionary (eval_data.txt.td)
