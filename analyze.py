import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
#Analyze text files
txtfiles = []
for dir_path,subpaths,files in os.walk('txtfiles'):
    for file in files:
        with open( os.path.join(dir_path, file), 'r') as f:
            txt = f.read()
            txtfiles.append(txt[:5000])
        break;
    break;

# compute tfidf vectors with scikits
v = TfidfVectorizer(input='content',
        encoding='utf-8', decode_error='replace', strip_accents='unicode',
        lowercase=True, analyzer='word', stop_words='english',
        token_pattern=r'(?u)\b[a-zA-Z_][a-zA-Z0-9_]+\b',
        ngram_range=(1, 2), max_features = max_features,
        norm='l2', use_idf=True, smooth_idf=True, sublinear_tf=True,
max_df=1.0, min_df=1)


v.fit(txtfiles)
X = v.transform(txtfiles)
print(v.vocabulary_)
print(X.shape)
