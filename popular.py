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
    data = pd.concat([pd.read_csv(f) for f in glob.glob('./data/*.csv')],ignore_index=True)

    tokenizer = TweetTokenizer()
    vectorizer = TfidfVectorizer(tokenizer=tokenizer.tokenize)
    response = vectorizer.fit_transform(data['Status'])
    feature_names = vectorizer.get_feature_names()
    weight = vectorizer.idf_
    feature_array = np.array(feature_names)
    tfidf_sorting = np.argsort(response.toarray()).flatten()[::-1]
    n = 100
    top_n = feature_array[tfidf_sorting][:n]
    #print(top_n)
    #tfidf_scores = dict(zip(feature_names, weight))
    #print(tfidf_scores)
    with open('topn.txt', 'w') as f:
        for word in top_n:
            f.write(word + '\n')

if __name__ == '__main__':
    trending_words()
