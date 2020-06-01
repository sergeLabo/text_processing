#!/usr/bin/env python3.7


import os
import re
import json
import nltk
from nltk.stem.snowball import FrenchStemmer
import pandas as pd
import matplotlib.pyplot as plt
import statistics
from collections import OrderedDict
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn import manifold

"""
title, livre, fable sont des str

    corpus = { livre-1: {title: fable,
                         title1: fable1},
               livre-2: ...
             }
"""

def get_corpus():
    """Le corpus est le fichier corpus.json"""

    fichier = "corpus.json"
    with open(fichier) as f:
        data = f.read()
    f.close()
    return json.loads(data)

def get_livre_assemblage(corpus):
    """Regroupe les fables par livre
    livres = {livre1: str(des fables de 1),
              livre2: ....
             }
    """
    livres = {}
    for livre, val in corpus.items():
        if not livre in livres:
            livres[livre] = ""
        for title, fable in val.items():
            livres[livre] += fable + "\n"

    return livres

def get_bigram(corpus):
    """Bigrammes de NLTK"""

    livres = get_livre_assemblage(corpus)
    tokenizer = nltk.RegexpTokenizer(r'\w+')

    print(f'Bigrammes de NLTK:\n')
    for livre, text in livres.items():
        tokens = tokenizer.tokenize(text.lower())
        bigr = list(nltk.bigrams(tokens))
        print(f'{livre}: {bigr[:20]}\n')

def get_tf_idf(corpus, sw):
    """Term-Frequency - Inverse Document Frequency"""

    livres = get_livre_assemblage(corpus)
    tokenizer = nltk.RegexpTokenizer(r'\w+')

    tf_idf, token_dict = {}, {}

    print(f'\nTF-IDF:\n')
    tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words=sw)
    for livre, text in livres.items():
        # Suppression des ponctuations
        unpunkt = tokenizer.tokenize(text.lower())
        tf_idf[livre] = tfidf.fit_transform(unpunkt)

    return tf_idf

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    stemmer = FrenchStemmer()
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems

def t_SNE_vizualisation(tf_idf):
    """Vizualisation t-SNE"""

    print('Cette fonction est secrète')


def main():

    corpus = get_corpus()
    sw = nltk.corpus.stopwords.words('french')
    # #get_bigram(corpus)
    tf_idf = get_tf_idf(corpus, sw)
    t_SNE_vizualisation(tf_idf)


if __name__ == "__main__":
    main()
