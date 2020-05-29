#!/usr/bin/env python3.7

import nltk
from nltk.corpus import treebank

raw = """À Monseigneur Le Duc de Bourgogne
Prince, l’unique objet du soin des Immortels,
Souffrez que mon encens parfume vos Autels.
Je vous offre un peu tard ces présents de ma Muse ;
"""

# ### Récupération d'un texte
# Tokenize the text
tokens = nltk.wordpunct_tokenize(raw)
print(f'tokens:\n{tokens}')

# Je ne garde que du 2ème mot au 30ème
tokens =tokens[2:30]
print(f'Texte:\n{tokens}')

# ### Normalizing 1
# Création d'un NLTK Text
text = nltk.Text(tokens)
print(f'Texte:\n{text}')
# <Text: Bourgogne Prince , l ’ unique objet du...>

# Normalize the words
words = [w.lower() for w in text]
print(f'words: nombre={len(words)}\n{words}')

# Build vocabulary (les mots sans la ponctuation, apostrophe)
vocab = sorted(set(words))
print(f'vocab: nombre={len(vocab)}\n{vocab}')

# ### Normalizing 2
# Tous les mots sans exception
mots_brut = nltk.word_tokenize(raw)
print(f'\nTous les mots bruts = {mots_brut}\n')
print(f'\nNombre de mots brut = {len(mots_brut)}\n')

# Sans la ponctuation et apostrophes
tokenizer = nltk.RegexpTokenizer(r'\w+')
bons_mots = tokenizer.tokenize(raw.lower())
print(f'\nTous les bons mots = {bons_mots}\n')
print(f'\nNombre de bons mots = {len(bons_mots)}\n')

# Fréquence des mots, sans la ponctuation et apostrophes
tokenizer = nltk.RegexpTokenizer(r'\w+')
corpora = tokenizer.tokenize(raw.lower())
freq = nltk.FreqDist(corpora)
print(f'Fréquence des mots dans le désordre:')
for k, v in freq.items():
    print(f'    {k} {v}')

# ### Some simple things you can do with NLTK
tokens = nltk.word_tokenize(raw)
tagged = nltk.pos_tag(tokens)
print(f'tagged[0:6] = {tagged[0:6]}')

# Identify named entities
entities = nltk.chunk.ne_chunk(tagged)
print(f'entities = {entities}')

# Display a parse tree:
t = treebank.parsed_sents('wsj_0001.mrg')[0]
t.draw()
