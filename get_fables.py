#!/usr/bin/env python3.7


import os
from pathlib import Path
from bs4 import BeautifulSoup

"""
txt:
    ligne 1 = livre
    ligne 2 = titre
    ligne 3 et + = fable

<p class="fable">
        La Cigale, ayant chant&eacute;<br />
Tout l'&eacute;t&eacute;,<br />
Se trouva fort d&eacute;pourvue<br />
...
- Vous chantiez ? j'en suis fort aise.<br />
Eh bien! dansez maintenant.
</p>
"""


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

def write_data_in_file(data, fichier, mode="w"):
    with open(fichier, mode) as fd:
        fd.write(data)
    fd.close()

def read_file(file_name):
    """
    Retourne les datas lues dans le fichier avec son chemin/nom
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

def get_infos(html):
    """html = mesfables/livre-1/11-l-homme-et-son-image.html"""

    soup = BeautifulSoup(read_file(html), "lxml")
    fable = soup.find_all('p', class_='fable')[0].get_text()
    title = soup.title.get_text()
    livre = html.split('/')[1]

    return title, fable, livre

def save_in_txt(title, fable, livre):
    """
    ligne 1 = livre
    ligne 2 = titre
    ligne 3 et + = fable
    """
    data = livre + '\n' + title + '\n' + fable
    fichier = './fables_txt/' + title + '.txt'
    write_data_in_file(data, fichier)

def main():
    htmls = get_all_files_list("./mesfables", [".html"])

    for html in htmls:
        title, fable, livre = get_infos(html)
        save_in_txt(title, fable, livre)
    print('Done.')


if __name__ == "__main__":
    main()
