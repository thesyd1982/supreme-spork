"""
Simple Scraper
TODO:
recuperer les url interne dans dautre balises
"""
import random
import requests
from queue import Queue
import time
from models.webRessource import headers_base as headers
from bs4 import BeautifulSoup
from pprint import pprint

tempo = random.uniform(1.2, 1.8)
q = Queue()
result = []
url_base = "https://arnaudchochon.com/"


def get_default_domain_and_path(url):
    prefix, domain = url.split('//')
    path = prefix + "//"
    if '/' in domain:
        domain = domain.split('/')[0]
    if "www." in domain:
        domain = domain.replace('www.', '')
        path_base += "www."
    path += domain
    return domain, path


domain_base, path_base = get_default_domain_and_path(url_base)
q.put(url_base)

s = requests.Session()
s.headers.update(headers)
error = 0
error_limit = 20

while not q.empty():
    soup = None
    all_link = []
    url_now = q.get()

    try:
        print(url_now)
        soup = BeautifulSoup(s.get(url_now, headers=headers).content, 'lxml')
        error = 0
    except:
        error += 1
    if soup:
        all_link_soup = soup.find_all('a')
        for x in all_link_soup:
            try:
                if x['href'][:1] == "/":
                    all_link.append(path_base + x['href'])

                elif domain_base in get_default_domain_and_path(x['href'])[0]:
                    all_link.append(x['href'])
            except:
                pass
        all_link = list(set(all_link))
        for link in all_link:
            if link not in result:
                result.append(link)
                q.put(link)
        print('#'*100)
        print('result length')
        print(len(result))
        print('queue lenght')
        print(q.qsize())
        print('error')
        print(error)
        time.sleep(tempo)
        if error > error_limit:
            break

s.close()
result.sort()
pprint(result)
