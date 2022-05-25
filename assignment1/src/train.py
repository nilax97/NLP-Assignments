import pandas as pd
import numpy as np
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

if not sys.warnoptions:
    warnings.simplefilter("ignore")

train = sys.argv[1];
dev = sys.argv[2];
model = sys.argv[3];

yelp_train = pd.read_json(train, lines=True);
yelp_dev = pd.read_json(dev, lines=True);
yelp_megatrain = yelp_train.append(yelp_dev);

X_train = yelp_megatrain['review'];
y_train = yelp_megatrain['ratings'];

text_clf = Pipeline([
    ('tfidf',TfidfVectorizer(preprocessor=None,
                             tokenizer=word_tokenize,
                             analyzer='word',
                             stop_words=None,
                             strip_accents=None,
                             lowercase=True,
                             ngram_range=(1,3),
                             min_df=0.0001,
                             max_df=0.9,
                             binary=False,
                             norm='l2',
                             use_idf=1,
                             smooth_idf=1,
                             sublinear_tf=1)),
    ('clf', LogisticRegression(penalty='l2',
                               solver='saga',
                               multi_class='multinomial',
                              tol=1e-5,
                              n_jobs = -1)),
]);

text_clf.fit(X_train,y_train);

pickle.dump(text_clf, open(model, "wb"));