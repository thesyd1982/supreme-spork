"""
Simple Crawler
TODO:
-mulithread ?
-pouvoir interrompre avec ctrl+c
-tri resultat par type content,(image,styles,page,other,special(tel,email))
-recuperer les ressource distant (hors domaine) mais ne pas les ajouter a la queue et les mettre dnas une liste special que si demander avce un arguments
-trier les images le style et les script js avec leur extension presente dans le path de lurl
"""
__author__ = "Antoine Chauvin"
__copyright__ = "Copyright (C) 2021 Antoine Chauvin"
__license__ = "Public Domain"
__version__ = "1.0"

import time
import random
import urllib.parse
from queue import Queue

import requests
from bs4 import BeautifulSoup

from models.outputFile import save_json
from models.timePrint import print_timep
from models.webRessource import URL
from models.webRessource import headers_crawler as headers

banner = """ _       __       __       ______                        __                     ___
| |     / /___   / /_     / ____/_____ ____ _ _      __ / /___   _____   _   __<  /
| | /| / // _ \\ / __ \\   / /    / ___// __ `/| | /| / // // _ \\ / ___/  | | / // / 
| |/ |/ //  __// /_/ /  / /___ / /   / /_/ / | |/ |/ // //  __// /      | |/ // /  
|__/|__/ \\___//_.___/   \\____//_/    \\__,_/  |__/|__//_/ \\___//_/       |___//_/   

"""


class WebCrawler:
    def __init__(self, url_base, path_output=None, verbose=True, error_limit=10, tempo=None, local_only=True):
        # Init variables
        self.url_base = url_base
        self.path_output = path_output
        self.verbose = verbose
        self.local_only = local_only
        self.error_limit = error_limit
        self.time_start = None
        self.url_now = None
        self.url_last = None
        self.r = None
        self.h = None
        self.default_tempo = [1, 2]

        # Initaliser la Queue
        self.q = Queue()

        # Ajouter l'URL de base
        self.q.put(url_base)
        self.result = []
        self.result_styles = []
        self.result_images = []
        self.result_special = []
        self.result_other = []
        self.error, self.erreur_total, self.nbr_requete = 0, 0, 0
        self.append_result_start = 0
        self.append_req_start = 0

        # Récuperer le domaine de base et le chemin par defaut
        url_o = URL(url_base)
        self.domain_base = url_o.domain_pur
        self.path_base = url_o.root_path

        # Init la session
        self.s = requests.Session()
        self.s.headers.update(headers)

        # Init Tempo
        if not tempo:
            tempo = self.default_tempo
        self.tempa = random.uniform(tempo[0], tempo[1])
        print('[ * ] Tempo : {} s - {} s'.format(tempo[0], tempo[1]))

    def print_verbose(self):
        append_result = len(self.result) - self.append_result_start
        if append_result > 0:
            append_result = "+{}".format(append_result)
        append_req = (self.q.qsize() - self.append_req_start) + 1
        if append_req > 0:
            append_req = "+{}".format(append_req)
        try:
            requests_per_second = round(self.nbr_requete / int(time.time() - self.time_start), 2)
        except ZeroDivisionError:
            requests_per_second = 0
        try:
            temps_restant_estime = int(self.q.qsize() / requests_per_second)
        except ZeroDivisionError:
            temps_restant_estime = 0

        print('URL: {}'.format(self.url_last))
        print('Requests: {}'.format(self.nbr_requete))
        print('Results: {} [{}]'.format(len(self.result), append_result))
        print('To do: {} [{}]'.format(self.q.qsize(), append_req))
        print("Consecutive error: {}".format(self.error))
        print("Error: {}".format(self.erreur_total))
        print("Speed: {} r/s".format(requests_per_second))
        print("Minimum time: {}".format(print_timep(temps_restant_estime)))
        print("Time elapsed : {}".format(print_timep(int(time.time() - self.time_start))))

    def parse_page(self):
        if self.verbose:
            print('#' * 100)
        # Remettre par defaut les variables
        soup = None

        # Essayer de recupérer le contenu de la page
        try:
            self.error = 0
            self.h = self.s.head(self.url_now, headers=headers, allow_redirects=True)
            self.nbr_requete += 1

            if self.h.url != self.url_now:
                if URL(self.h.url).domain_pur in URL(self.url_now).domain_pur:
                    self.url_now = self.h.url

            # Exclure les medias pour le scrap et les pages 404
            content_type = self.h.headers['Content-Type']
            if 'text/html' in content_type:
                if self.h.status_code != 404:
                    self.r = self.s.get(self.url_now, headers=headers)
                    self.nbr_requete += 1
                    soup = BeautifulSoup(self.r.content, 'lxml')
                else:
                    print("No download content because 404 page")
            else:
                if 'css' in content_type:
                    self.result_styles.append(self.url_now)
                elif 'image' in content_type:
                    self.result_images.append(self.url_now)
                print("No download content because content-type: " + content_type)
        except requests.exceptions.RequestException:
            self.error += 1
            self.erreur_total += 1

        # if soup to scrap
        if soup:

            # Récuperation de toutes les balise de liens
            all_link_soup_a = [{'attr': 'href', 'object': x} for x in soup.find_all('a')]
            all_link_soup_link = [{'attr': 'href', 'object': x} for x in soup.find_all('link')]
            all_link_soup_img = [{'attr': 'src', 'object': x} for x in soup.find_all('img')]
            all_link_soup_script = [{'attr': 'src', 'object': x} for x in soup.find_all('script')]
            all_link_soup_embed = [{'attr': 'src', 'object': x} for x in soup.find_all('embed')]
            all_link_soup_iframe = [{'attr': 'src', 'object': x} for x in soup.find_all('iframe')]
            all_link_soup_input = [{'attr': 'src', 'object': x} for x in soup.find_all('input')]
            all_link_soup_source = [{'attr': 'src', 'object': x} for x in soup.find_all('source')]
            all_link_soup_track = [{'attr': 'src', 'object': x} for x in soup.find_all('track')]
            all_link_soup_video = [{'attr': 'src', 'object': x} for x in soup.find_all('video')]
            all_link_soup = all_link_soup_a + all_link_soup_link + all_link_soup_img + all_link_soup_script + all_link_soup_embed + all_link_soup_iframe + all_link_soup_input + all_link_soup_source + all_link_soup_track + all_link_soup_video

            # Traitement des liens récuperer
            for y in all_link_soup:
                try:
                    x = y['object'][y['attr']]

                    # Si l'attribut n'est pas vide
                    if x != "":
                        url_x = URL(x, self.url_now)
                        if self.domain_base in url_x.domain_pur:
                            if url_x.real_loc not in self.result and not url_x.is_js:
                                # Enlever les doublons d'encodage
                                if urllib.parse.unquote(url_x.real_loc) not in self.result and urllib.parse.quote(url_x.real_loc, safe='') not in self.result and urllib.parse.quote(url_x.real_loc) not in self.result:
                                    self.result.append(url_x.real_loc)
                                    if y['attr'] == 'href':
                                        # Ne pas ajouter les urls speciales et les ancres au requetes suivante
                                        if not url_x.is_special:
                                            if not url_x.is_anchor:
                                                self.q.put(url_x.real_loc)
                                        else:
                                            self.result_special.append(url_x.real_loc)
                except AttributeError:
                    pass
                except KeyError:
                    pass

    def explore_website(self):
        # Calcul du temps
        self.time_start = time.time()
        self.result.append(self.url_base)

        try:
            # Tant que la liste d'url a crawler n'est pas vide
            while not self.q.empty():
                self.append_result_start = len(self.result)
                self.append_req_start = self.q.qsize()

                self.url_last = self.url_now

                # récuperer la prochaine url
                self.url_now = self.q.get()

                # Parse la page
                self.parse_page()
                # Affichage
                if self.verbose:
                    self.print_verbose()


                # Break si le nombre d'erreurs max est depasse
                if self.error > self.error_limit:
                    print(" + ] Nombre d'erreur limite atteinte")
                    break

                # Tempo de la boucle
                time.sleep(self.tempa)

        except KeyboardInterrupt:
            print('[*] Crawl Stopped !')

        # Fermer la session
        self.s.close()

        # Trier les résultats
        self.result = list(set(self.result) - set(self.result_images))
        self.result = list(set(self.result) - set(self.result_styles))
        self.result = list(set(self.result) - set(self.result_special))
        self.result.sort()

        # Output Format
        dict_output = {'url_base': self.url_base,
                       'req_count': self.nbr_requete,
                       'res_count': len(self.result),
                       'err_count': self.erreur_total,
                       'crawl_time': round(time.time() - self.time_start, 2),
                       'result': self.result,
                       'styles': self.result_styles,
                       'images': self.result_images,
                       'contact': self.result_special,
                       'other': self.result_other}
        # Output file
        if self.path_output:
            save_json(self.path_output, dict_output)

        print('[ * ] Crawl Terminé')
        return dict_output


if __name__ == "__main__":
    print(banner)
    url = input("URL >> ")
    webcrwl = WebCrawler(url, "output25.json", tempo=[0.21,0.32])
    webcrwl.explore_website()
