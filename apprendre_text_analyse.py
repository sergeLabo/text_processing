#!/usr/bin/env python3.7


import os
import json

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

"""
corpus[title] = [livre, fable]
"""

def read_file(file_name):
    """Retourne les datas lues dans le fichier avec son chemin/nom
    Retourne None si fichier inexistant ou impossible à lire .
    """

    try:
        with open(file_name) as f:
            data = f.read()
        f.close()
    except:
        data = None
        print("Fichier inexistant ou impossible à lire:", file_name)

    return data


def get_corpus():
    corpus = json.loads(read_file('corpus.json'))

    stop_words = set(stopwords.words('french'))
    my_values = [",", ".", ";"]
    for mv in my_values:
        stop_words.add(mv)
    print("stop_words =", stop_words)

    tokens = nltk.word_tokenize(big_text)
    tokens = [w for w in tokens if not w in stop_words]


    vocabulary = set(tokens)
    print(len(vocabulary))   # avec accent 25302 sans accent 24549
    frequency_dist = nltk.FreqDist(tokens)

    print(sorted(frequency_dist,
                 key=frequency_dist.__getitem__,
                 reverse=True)[0:100])

def main():
    corpus = get_corpus()


if __name__ == "__main__":
    main()
