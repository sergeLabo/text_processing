#!/usr/bin/env python3.7


import os
from pathlib import Path
import json


def write_data_in_file(data, fichier, mode="w"):
    with open(fichier, mode) as fd:
        fd.write(data)
    fd.close()

def get_all_files_list(directory, extentions):
    """
    Lit le dossier et tous les sous-dosssiers.
    Retourne la liste de tous les fichiers avec les extentions de
    la liste extentions.
    """

    file_list = []
    for path, subdirs, files in os.walk(directory):
        for name in files:
            for extention in extentions:
                if name.endswith(extention):
                    file_list.append(str(Path(path, name)))

    return file_list

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
    files = get_all_files_list("./fables_txt", [".txt"])
    corpus = {}
    for f in files:
        text = read_file(f)
        t = text.splitlines()
        livre = t[0]
        title = t[1]
        fable = t[2:]
        corpus[title] = [livre, fable]

    return corpus

def main():
    corpus = get_corpus()
    write_data_in_file(json.dumps(corpus), 'corpus.json')


if __name__ == "__main__":
    main()
