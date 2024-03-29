"""
Script qui explore un site web avec une wordlist
"""
import requests
import time
from models.webRessource import headers_base as headers


def test_wordlist(url, path_listWord, tempo=0.5):
    with open(path_listWord, 'r') as rFile:
        liste_word = [x.strip() for x in rFile.readlines()]

    for word in liste_word:
        r = requests.get(url + word, headers=headers)
        if r.status_code != 404:
            print("[ + ] {}{} [{}] {}".format(url, word, r.status_code, r.reason))
        time.sleep(tempo)


if __name__ == "__main__":
    test_wordlist("http://challenge01.root-me.org/web-serveur/ch4/", 'list.txt')
