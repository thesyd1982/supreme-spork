"""
Script Permettant de récuperer le contenu d'une page avec une mauvaise redirection
"""

import requests

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}


def get_content(url):
    return requests.get(url, headers=headers, allow_redirects=False).content


if __name__ == "__main__":
    print(get_content('http://challenge01.root-me.org/web-serveur/ch32/').decode())
