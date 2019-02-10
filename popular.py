import pandas as pd
import numpy as np
import csv
import logging
import nltk
import os
import glob
from nltk.tokenize import TweetTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from operator import itemgetter

def trending_words():
    """
    Get top 100 trending words from our data and saves in the topn.txt file
    """
    data = pd.concat([pd.read_csv(f) for f in glob.glob('./data/*.csv')],
                     ignore_index=True)

    tokenizer = TweetTokenizer()
    vectorizer = TfidfVectorizer(tokenizer=tokenizer.tokenize,ngram_range=(1,2))
    response = vectorizer.fit_transform(data['Status'])    # Map feature index to feature name
    feature_names = vectorizer.get_feature_names()    #  weight is the tf-idf value
    weight = vectorizer.idf_
    #soring the weights
    indices = np.argsort(weight)[::-1]
    top_weights = 400
    top_features = [feature_names[i] for i in indices[:top_weights]]
    with open('topn.txt', 'w') as f:
        for word in top_features:
            f.write(word + '\n')

if __name__ == '__main__':
    trending_words()
