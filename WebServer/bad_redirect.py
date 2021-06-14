"""
Script Permettant de récuperer le contenu d'une page avec une mauvaise redirection
"""
import requests
from models.webRessource import headers_base as headers


def get_content(url):
    return requests.get(url, headers=headers, allow_redirects=False).content


if __name__ == "__main__":
    print(get_content('http://challenge01.root-me.org/web-serveur/ch32/').decode())
