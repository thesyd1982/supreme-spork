"""
Script Permettant de récuperer le contenu d'une page avec une mauvaise redirection
"""

import requests


def get_content(url):
    return requests.get(url, allow_redirects=False).content


if __name__ == "__main__":
    print(get_content('http://challenge01.root-me.org/web-serveur/ch32/').decode())