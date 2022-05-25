import gensim
from gensim.models import Word2Vec, word2vec, KeyedVectors
import numpy as np
import os
import sys
import warnings
import string
import multiprocessing
import string
import pickle
import pandas as pd
if not sys.warnoptions:
	warnings.simplefilter("ignore")

import nltk
nltk.download('averaged_perceptron_tagger');
nltk.download('punkt');
from nltk import word_tokenize, pos_tag

input_data_folder = sys.argv[1];
model_path = sys.argv[2];
pretrained_embeddings = sys.argv[3];
eval_file_name = sys.argv[4];
target_file_name = sys.argv[5];

eval_file = open(eval_file_name, "r");
input = eval_file.readlines();

output = open(input_data_folder + "dataset.txt", "w");

for line in input:
	x = line.strip().replace("<<target>>","$$NILAKSH$$").replace("::::", "$$NILAKSH$$").split("$$NILAKSH$$")
	temp = x[0] + x[2] + x[1]+'\n';
	output.write(temp);
output.close();

class MySentences(object):
	def __init__(self, dirname):
		self.dirname = dirname
 
	def __iter__(self):
		for fname in os.listdir(self.dirname):
			if(fname == '.DS_Store'):
				continue;
			for line in open(os.path.join(self.dirname, fname)):
				if(len(line)>0):
					yield word_tokenize(line);
				
sentences = MySentences(input_data_folder)

model = Word2Vec(sentences, 
				 size = 300, 
				 iter = 10, 
				 sg = 1, 
				 window = 5, 
				 hs = 0, 
				 negative = 5, 
				 ns_exponent = 0.75, 
				 min_count = 0, 
				 workers = multiprocessing.cpu_count());

model.intersect_word2vec_format(pretrained_embeddings, lockf=1.0, binary=True);

model.train(sentences, total_examples=model.corpus_count, epochs=250);

pickle.dump(model, open(model_path, "wb"));