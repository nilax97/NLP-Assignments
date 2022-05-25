import pandas as pd
import numpy as np
import scipy
import re
import string
import json
import nltk
import sklearn
import pickle
import sys
import warnings

nltk.download('punkt')

from nltk import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report,confusion_matrix, accuracy_score, mean_squared_error

if not sys.warnoptions:
    warnings.simplefilter("ignore")

model = sys.argv[1];
test = sys.argv[2];
output_file = sys.argv[3];

yelp_test = pd.read_json(test, lines=True);
X_test = yelp_test['review'];
y_test = yelp_test['ratings'];

text_clf = pickle.load(open(model,"rb"))

pred = text_clf.predict(X_test);
np.savetxt(output_file , pred, fmt='%1.2f');