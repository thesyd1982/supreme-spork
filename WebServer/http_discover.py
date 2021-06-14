"""
Script qui explore un site web avec une wordlist
"""
import requests
import time

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}


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
