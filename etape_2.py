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
    for livre, text in corpus.items():
        if not livre in livres:
            livres[livre] = ""
        for title, fable in text.items():
            livres[livre] += fable + "\n"

    return livres

def get_stopwords(corpus):
    """Stopwords = mots très courants dans la langue
    ("et", "à", "le"... en français) qui n'apportent pas de valeur informative.
    Il seront supprimés du texte.

    Aux stopwords 'french', seront ajoutés arbitrairement, les mots les plus
    fréquents du texte.

    100 = nombre de mots les plus fréquents non retenu pour l'étude
    """

    # Mots très utilisés par l'auteur
    number = 100
    livres = get_livre_assemblage(corpus)  # dict par livre

    # Tous les livres dans un str
    all_fables = ""
    for k, v in livres.items():
        all_fables += v + '\n'

    # Fréquence de tous les mots en désordre
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    corpora = tokenizer.tokenize(all_fables.lower())
    freq = nltk.FreqDist(corpora)

    # Tri des fréquence de tous les mots, et on garde seulement les 100 1er
    most_freq = OrderedDict()
    n = 0
    for k in sorted(freq, key=freq.get, reverse=True):
        if n < number:
            most_freq[k] = freq[k]
        n += 1
    print('\n\nLes mots les plus fréquents:')
    for k, v in most_freq.items():
        print(f'    {k} {v}')
    print('\n\n')

    # Ajout des 2 stopwords: most_freq et stopwords 'french'
    sw = set()
    sw.update(most_freq)
    print(f'Nombre de stopwords des fables = {len(sw)}')
    fr = nltk.corpus.stopwords.words('french')
    print(f'Nombre de stopwords FR = {len(fr)}')
    sw.update(tuple(fr))
    print(f'Nombre de stopwords = {len(sw)}')
    print('Stopwords:')
    print(f'    {sw}')
    return sw

def words_frequency_without_stopwords(corpus, sw):
    """bag-of-words = Sac de mots
    Chaque mot se voit affecté le nombre de fois qu'il apparaît dans le
    document = richesse du vocabulaire par livre
    """

    livres = get_livre_assemblage(corpus)
    freqs_with, freqs_without, stats = {}, {}, {}
    tokenizer = nltk.RegexpTokenizer(r'\w+')

    for livre, text in livres.items():
        tokens = tokenizer.tokenize(text.lower())
        freqs_with[livre] = fq_with = nltk.FreqDist(tokens)
        corpora = [w for w in tokens if w not in list(sw)]
        freqs_without[livre] = fq_without = nltk.FreqDist(corpora)
        stats[livre] = {'Nombre de mots au total': len(tokens),
                        'Vocabulaire avec les mots courants': len(fq_with.keys()) ,
                        'Vocabulaire sans les mots courants': len(fq_without.keys())
                        }

        print(f'{livre}\
              \nNombre de mots au total {len(tokens)}\
              \nVocabulaire sans les mots courants: {len(fq_with.keys())}\
              \nVocabulaire sans les mots courants: {len(fq_without.keys())}')

    # Affichage des nombres de mots par livre
    df = pd.DataFrame.from_dict(stats, orient='index')
    df = df.sort_values(by=['Nombre de mots au total'], ascending=False)
    df.plot(kind='bar', color=["#FF00FF", "#FF0000", "#00FF2B"],
            title='Fréquence des mots par livre sans stopwords')
    plt.show()

def racinisation(corpus, sw):
    """La racine d’un mot correspond à la partie du mot restante une fois que
    l’on a supprimé son (ses) préfixe(s) et suffixe(s), à savoir son radical.
    chercher a pour radical cherch
    Cette fonction supprime les stopwords
    """

    stemmer = FrenchStemmer()
    livres = get_livre_assemblage(corpus)
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    stats, freq, corpora = {}, {}, {}

    for livre, text in livres.items():
        if livre not in corpora:
            corpora[livre] = []
        tokens = tokenizer.tokenize(text.lower())
        corpora[livre] += [stemmer.stem(w) for w in tokens if not w in list(sw)]

    for livre, text in corpora.items():
        freq[livre] = fq = nltk.FreqDist(text)
        stats[livre] = {'Nombre de mots au total': len(text),
                        'Après racinisation': len(fq.keys())}

    # Affichage des nombres de mots par livre
    df = pd.DataFrame.from_dict(stats, orient='index')
    df = df.sort_values(by=['Nombre de mots au total'], ascending=False)
    df.plot(kind='bar', color=["#FF00FF", "#00FF2B"],
            title='Fréquence des mots après racinisation')
    plt.show()

    return stats, freq, corpora


def main():

    corpus = get_corpus()
    sw = get_stopwords(corpus)
    words_frequency_without_stopwords(corpus, sw)
    stats, freq, corpora = racinisation(corpus, sw)


if __name__ == "__main__":
    main()
