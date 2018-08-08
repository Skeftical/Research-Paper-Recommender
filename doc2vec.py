
# coding: utf-8

# In[1]:

import pandas as pd
import gensim
import os
import collections
import smart_open
import random
import numpy as np


# In[2]:

df = pd.read_csv(open('library.corr','rU'), encoding='utf8',header=None, engine='c',delimiter=',', error_bad_lines=False, low_memory=False, index_col=None)


# In[3]:

df = df[[0,1,2]].dropna()


# In[4]:

corpus = []
for index, row in df.iterrows():
    tagged_d = gensim.models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(row[2]), [index])
    corpus.append(tagged_d)


# In[5]:

train = corpus[:int(len(corpus)*0.8)]
test = corpus[int(len(corpus)*0.8):]


# In[6]:

model = gensim.models.doc2vec.Doc2Vec(size=75, min_count=2, iter=1000)
model.build_vocab(train)


# In[7]:

model.train(train, total_examples=model.corpus_count, epochs=model.iter)

model.save('modelDoc2Vec.model')
