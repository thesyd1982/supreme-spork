"""
Simple Crawler
TODO:
-ne pas scrap le contenu des media, du js, du css, ect...
-mulithread ?
-liste en entree
-pouvoir interrompre avec ctrl+c
-rajouter balise :
embed['src']
iframe['src']
input['src']
source['src']
track['src']
video['src']

-ajouter des statistique (combien de resultat en + par url,url a faire en plus par url analyser)
-ameliorer l'affichage et rajoueter une barrde progression sur : nombre de reqwuete faite / (nombre de requete faite + nombre de requeet a faire)


"""
import random
import requests
from queue import Queue
import time
from models.webRessource import headers_crawler as headers
from models.webRessource import URL
from models.timePrint import print_timep
from models.outputFile import save_json
from bs4 import BeautifulSoup


class WebCrawler:
    def __init__(self, url_base, path_output=None, verbose=True, error_limit=10, tempo=None):
        # Init variables
        self.url_base = url_base
        self.path_output = path_output
        self.verbose = verbose
        self.error_limit = error_limit
        self.time_start = None
        self.url_now = None
        self.r = None
        self.default_tempo = [1, 2]

        # Initaliser la Queue
        self.q = Queue()

        # Ajouter l'URL de base
        self.q.put(url_base)
        self.result = []
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
        if append_result < 0:
            append_result = "+{}".format(append_result)
        append_req = (self.q.qsize() - self.append_req_start)+1
        if append_req < 0:
            append_req = "+{}".format(append_req)
        try:
            requests_per_second = round(self.nbr_requete / int(time.time() - self.time_start),2)
        except ZeroDivisionError:
            requests_per_second = 0
        try:
            temps_restant_estime = int(self.q.qsize() / requests_per_second)
        except ZeroDivisionError:
            temps_restant_estime = 0

        print('#' * 100)
        print('URL Content Scraped : {}'.format(self.url_now))
        print('Nombre de requete : {}'.format(self.nbr_requete))
        print('Nombre de résultat : {} [{}]'.format(len(self.result), append_result))
        print('Nombre de requetes restantes : {} [{}]'.format(self.q.qsize(), append_req))
        print("Nombre d'erreur consecutives : {}".format(self.error))
        print("Nombre d'erreur total : {}".format(self.erreur_total))
        print("Nombre de requetes par seconde : {} r/s".format(requests_per_second))
        print("Temps restant estimé : {}".format(print_timep(temps_restant_estime)))
        print("Temps : {}".format(print_timep(int(time.time() - self.time_start))))


    def explore_website(self):
        # Calcul du temps
        self.time_start = time.time()

        # Tant que la liste d'url a crawler n'est pas vide
        try:
            while not self.q.empty():
                # Remettre par defaut les variables
                soup = None
                self.append_result_start = len(self.result)
                self.append_req_start = self.q.qsize()

                # récuperer la prochaine url
                self.url_now = self.q.get()

                # Essayer de recupérer le contenu de la page
                try:
                    self.r = self.s.get(self.url_now, headers=headers)
                    self.nbr_requete += 1
                    self.error = 0

                    # Exclure les medias pour le scrap et les pages 404
                    if 'text/html' in self.r.headers['Content-Type']:
                        if self.r.status_code != 404:
                            soup = BeautifulSoup(self.r.content, 'lxml')
                        else:
                            print("No scrap content because 404 page")
                    else:
                        print("No scrap content because content-type: " + self.r.headers['Content-Type'])
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
                    all_link_soup = all_link_soup_a + all_link_soup_link + all_link_soup_img + all_link_soup_script
                    # all_link_soup_meta = [{'attr': 'content', 'object': x} for x in soup.find_all('meta')]

                    # Traitement des liens récuperer
                    for y in all_link_soup:
                        try:
                            x = y['object'][y['attr']]
                            url_x = URL(x, self.url_now)
                            if self.domain_base in url_x.domain_pur:
                                if url_x.real_loc not in self.result:
                                    self.result.append(url_x.real_loc)
                                    if y['attr'] == 'href':
                                        self.q.put(url_x.real_loc)
                        except AttributeError:
                            pass
                        except KeyError:
                            pass

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
        self.result.sort()

        # Output Format
        dict_output = {'url_base': self.url_base,
                       'req_count': self.nbr_requete,
                       'res_count': len(self.result),
                       'err_count': self.erreur_total,
                       'crawl_time': round(time.time() - self.time_start, 2),
                       'result': self.result}
        # Output file
        if self.path_output:
            save_json(self.path_output, dict_output)

        print('[ * ] Crawl Terminé')
        return dict_output


if __name__ == "__main__":
    url = input("url: ")
    webcrwl = WebCrawler(url, "output25.json", tempo=[0.2, 0.5])
    webcrwl.explore_website()
