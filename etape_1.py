#!/usr/bin/env python3.7


import os
import re
import json
import nltk
import pandas as pd
import matplotlib.pyplot as plt
import statistics
from collections import OrderedDict

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

def get_all_words(corpus):
    """Nombre de mots par fables sans exception, dans un dict
    nb_mots = {livre1: [nb_de_mots, 129, 241 ...], livre2: ...}
    """

    nb_mots = {}

    # Recherche du nombre de mots par fable
    for livre, val in corpus.items():
        if not livre in nb_mots:
            nb_mots[livre] = []
        for title, fable in val.items():
            mots_brut = nltk.word_tokenize(fable)
            nb_mots[livre].append(len(mots_brut))

    # Calcul de la moyenne par livre
    average_by_livre = {}
    for livre, val in nb_mots.items():
        average_by_livre[livre] = int(statistics.mean(val))
    print(f'Moyenne par livre brute:\n{average_by_livre}')
    # Tri et print
    sorted_my_dict(average_by_livre, 'Nombre de mots par livre')

def get_words_without_punkt(corpus):
    """Nombre de mots par fables sans ponctuation, dans un dict
    nb_mots = {livre1: [nb_de_mots, 129, 241 ...], livre2: ...}
    """

    nb_mots = {}
    tokenizer = nltk.RegexpTokenizer(r'\w+')

    # Recherche du nombre de mots par fable
    for livre, val in corpus.items():
        if not livre in nb_mots:
            nb_mots[livre] = []
        for title, fable in val.items():
            bons_mots = tokenizer.tokenize(fable.lower())
            nb_mots[livre].append(len(bons_mots))

    # Calcul de la moyenne par livre
    average_by_livre = {}
    for livre, val in nb_mots.items():
        average_by_livre[livre] = int(statistics.mean(val))
    print(f'Moyenne par livre brute:\n{average_by_livre}')
    # Tri et print
    sorted_my_dict(average_by_livre,
                    'Nombre de mots par livre sans ponctuation')

def sorted_my_dict(my_dict, titre):
    """Trie le dict sur les valeurs, print, et affichage de l'histogramme."""

    nb_mots = OrderedDict()
    for k in sorted(my_dict, key=my_dict.get, reverse=True):
        nb_mots[k] = my_dict[k]
    print('\nDictionnaire trié:')
    for k, v in nb_mots.items():
        print(f'    {k} {v}')

    # Affichage des nombres de mots par livre
    df = pd.DataFrame.from_dict(nb_mots, orient='index')
    df.plot(kind='bar', color="#f56900", title=titre)
    plt.show()

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
            livres[livre] += fable

    return livres

def words_total(corpus):
    """Nombre de mots total, sans la ponctuation et apostrophes, par livre."""

    livres = get_livre_assemblage(corpus)
    freqs = {}
    stats = {}
    tokenizer = nltk.RegexpTokenizer(r'\w+')

    for livre, val in livres.items():
        corpora = tokenizer.tokenize(val.lower())
        freqs[livre] = nltk.FreqDist(corpora)
        stats[livre] = {'total': len(val)}

    # Affichage des nombres de mots par livre
    df = pd.DataFrame.from_dict(stats, orient='index')
    # TODO pas de tri !
    # #df.sort_index(axis=1, ascending=False)
    df.plot(kind='bar', color="#f56900",
            title='Nombre de mots par livre sans ponctuation')
    plt.show()

def words_frequency(corpus):
    """bag-of-words = richesse du vocabulaire par livre"""

    livres = get_livre_assemblage(corpus)
    freqs = {}
    stats = {}
    tokenizer = nltk.RegexpTokenizer(r'\w+')

    for livre, val in livres.items():
        corpora = tokenizer.tokenize(val.lower())
        freqs[livre] = fq = nltk.FreqDist(corpora)
        stats[livre] = {'total': len(val), 'unique': len(fq.keys())}

    # Affichage des nombres de mots par livre
    df = pd.DataFrame.from_dict(stats, orient='index')
    # TODO pas de tri !
    # #df.sort_index(axis=1, ascending=False)
    # TODO revoir couleur
    df.plot(kind='bar', color="#f56900",
            title='Fréquence des mots par livre sans ponctuation')
    plt.show()

def get_stopwords(text, number):
    """Stopwords = mots très courants dans la langue
    ("et", "à", "le"... en français) qui n'apportent pas de valeur informative.
    Il seront supprimés du texte.

    Aux stopwords 'french', seront ajoutés arbitrairement, les mots les plus
    fréquents du texte.
    """

    tokenizer = nltk.RegexpTokenizer(r'\w+')
    corpora = tokenizer.tokenize(text.lower())
    freq = nltk.FreqDist(corpora)

    most_freq = OrderedDict()
    n = 0
    for k in sorted(freq, key=freq.get, reverse=True):
        if n < number:
            most_freq[k] = freq[k]
        n += 1
    print("\n\nLes mots les plus fréquents:")
    for k, v in most_freq.items():
        print(f'    {k} {v}')
    print("\n\n")

    # Ajout des 2 stopwords: most_freq et stopwords 'french'
    sw = set()
    sw.update(most_freq)
    sw.update(tuple(nltk.corpus.stopwords.words('french')))
    print("Stopwords:")
    print(f'    {sw}')
    return sw

def delete_most_frequency_words(text, sw):
    pass

def main():

    corpus = get_corpus()
    get_all_words(corpus)
    get_words_without_punkt(corpus)
    words_total(corpus)
    words_frequency(corpus)

    # ## 20 = nombre de mots les plus fréquent qui ne seront pas retenu pour l'étude
    # #sw = get_stopwords(corpus, 20)
    # #delete_most_frequency_words(corpus, sw)


if __name__ == "__main__":
    main()
