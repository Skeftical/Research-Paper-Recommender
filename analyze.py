import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from joblib import dump, load
from sklearn.svm import OneClassSVM
#Analyze text files
txtfiles = []
for dir_path,subpaths,files in os.walk('txtfiles'):
    for file in files:
        with open( os.path.join(dir_path, file), 'r') as f:
            txt = f.read()
            txtfiles.append(txt[:5000])

# compute tfidf vectors with scikits
v = TfidfVectorizer(input='content',
        encoding='utf-8', decode_error='replace', strip_accents='unicode',
        lowercase=True, analyzer='word', stop_words='english',
        token_pattern=r'(?u)\b[a-zA-Z_][a-zA-Z0-9_]+\b',
        ngram_range=(1, 2), max_features = 5000,
        norm='l2', use_idf=True, smooth_idf=True, sublinear_tf=True,
max_df=1.0, min_df=1)

v.fit(txtfiles)
X = v.transform(txtfiles)
print(v.vocabulary_)
print(X.shape)

dump(v, 'tfidf.model')
out = {}
out['X'] = X
print("writing", 'library.tfidf')
with open('library.tfid', 'wb') as f:
    pickle.dump(out, f)

out = {}
out['vocab'] = v.vocabulary_
out['idf'] = v._tfidf.idf_
print("writing", 'metadata.txt')
with open('meta_data.txt', 'wb') as f:
    pickle.dump(out, f)

#Build model
svm = OneClassSVM(kernel='rbf',gamma=0.01, nu=0.1)
svm.fit(X)
print(svm.predict(X))
dump(svm, 'svm.model')
