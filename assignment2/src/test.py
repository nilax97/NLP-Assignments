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

eval_file_name = sys.argv[1];
target_file_name = sys.argv[2];
model_path = sys.argv[3];
pretrained_embeddings = sys.argv[4];

old_model = KeyedVectors.load_word2vec_format(pretrained_embeddings, binary=True);

model = pickle.load(open(model_path,"rb"))

eval_file = open(eval_file_name, "r");
eval_lines = eval_file.readlines();

target_file = open(target_file_name, "r");
target_lines = target_file.readlines();

def dist(i,m):
	return 1;

output = open("output.txt", "w");
for line,words in zip(eval_lines, target_lines):
	line = line.strip().replace("<<target>>","$$NILAKSH$$").replace("::::", "$$NILAKSH$$").split("$$NILAKSH$$")
	w1 = np.zeros(300);
	w2 = np.zeros(300);
	l_words = word_tokenize(line[0])[::-1];
	r_words = word_tokenize(line[1]);
	m1 = len(l_words);
	m2 = len(r_words);
	for i in range(m1):
		if(l_words[i] in model.wv.vocab):
			w1 += dist(i,m1) * model.wv[l_words[i]];
	for i in range(m2):
		if(r_words[i] in model.wv.vocab):
			w2 += dist(i,m2) * model.wv[r_words[i]];
	w1 /= np.linalg.norm(w1);
	w2 /= np.linalg.norm(w2);
	
	tar_words = words.split();
	ranks = np.zeros(len(tar_words));
	wpred = np.zeros(300);
	
	for i in range(len(tar_words)):
		tar = tar_words[i];
		vocab = model.wv.vocab;
		old_vocab = old_model.vocab;
		if(tar in vocab):
			wpred = model.wv[tar].copy();
			wpred /= np.linalg.norm(wpred);
			ranks[i] = np.dot(w1, wpred) + np.dot(w2, wpred);
		elif(tar.title() in vocab):
			tar = tar.title()
			wpred = model.wv[tar].copy();
			wpred /= np.linalg.norm(wpred);
			ranks[i] = np.dot(w1, wpred) + np.dot(w2, wpred);
		elif(tar.upper() in vocab):
			tar = tar.upper();
			wpred = model.wv[tar].copy();
			wpred /= np.linalg.norm(wpred);
			ranks[i] = np.dot(w1, wpred) + np.dot(w2, wpred);
		elif(tar in old_vocab):
			wpred = old_model[tar].copy();
			wpred /= np.linalg.norm(wpred);
			ranks[i] = np.dot(w1, wpred) + np.dot(w2, wpred);
		elif(tar.title() in old_vocab):
			tar = tar.title();
			wpred = old_model[tar].copy();
			wpred /= np.linalg.norm(wpred);
			ranks[i] = np.dot(w1, wpred) + np.dot(w2, wpred);
		elif(tar.upper() in old_vocab):
			tar = tar.upper();
			wpred = old_model[tar].copy();
			wpred /= np.linalg.norm(wpred);
			ranks[i] = np.dot(w1, wpred) + np.dot(w2, wpred);
		else:
			ranks[i] = -1000;

	rank_frame = pd.DataFrame(data = ranks, columns=["Sim"])
	rank_frame.sort_values(by=["Sim"], inplace=True, ascending=False)
	rank_frame.reset_index(inplace=True)
	rank_frame.reset_index(inplace=True)
	rank_frame.columns=["rank", "index", "sim"]
	rank_frame.sort_values(by="index", inplace=True)
	rank_index = rank_frame.values[:,0] 
	rank_index = rank_index.astype(int)
	for x in rank_index:
		output.write(str(x+1) + " ");
	output.write("\n");
output.close();