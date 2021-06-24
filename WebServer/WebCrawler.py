"""
Simple Crawler
TODO:
-ne pas recuperer le contenu des media, du js, du css, ect...
-rajouter le status de la requete dans le result ?
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
from models.webRessource import headers_base as headers
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
        self.default_tempo = [1, 2]

        # Initaliser la Queue
        self.q = Queue()

        # Ajouter l'URL de base
        self.q.put(url_base)
        self.result = []
        self.error, self.erreur_total, self.nbr_requete = 0, 0, 0

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
        if self.q.empty():
            print('[ * ] Crawl Terminé')
        else:
            print('#' * 100)
            print('URL en cours : {}'.format(self.url_now))
            print('Nombre de requete : {}'.format(self.nbr_requete))
            print('Nombre de résultat : {}'.format(len(self.result)))
            print('Nombre de requetes restantes : {}'.format(self.q.qsize()))
            print("Nombre d'erreur consecutives : {}".format(self.error))
            print("Nombre d'erreur total : {}".format(self.erreur_total))
            print("Temps : {}".format(print_timep(int(time.time() - self.time_start))))

    def explore_website(self):
        # Calcul du temps
        self.time_start = time.time()

        # Tant que la liste d'url a crawler n'est pas vide
        try:
            while not self.q.empty():
                # Remettre par defaut les variables
                soup = None

                # récuperer la prochaine url
                self.url_now = self.q.get()

                # Essayer de recupérer le contenu de la page
                try:
                    soup = BeautifulSoup(self.s.get(self.url_now, headers=headers).content, 'lxml')
                    self.nbr_requete += 1
                    self.error = 0
                except requests.exceptions.RequestException:
                    self.error += 1
                    self.erreur_total += 1

                # Si il y a un contenu
                if soup:
                    # recuperer toutes les balise de liens
                    all_link_soup_a = [{'attr': 'href', 'object': x} for x in soup.find_all('a')]
                    all_link_soup_link = [{'attr': 'href', 'object': x} for x in soup.find_all('link')]
                    # all_link_soup_meta = [{'attr': 'content', 'object': x} for x in soup.find_all('meta')]
                    all_link_soup_img = [{'attr': 'src', 'object': x} for x in soup.find_all('img')]
                    all_link_soup_script = [{'attr': 'src', 'object': x} for x in soup.find_all('script')]
                    all_link_soup = all_link_soup_a + all_link_soup_link + all_link_soup_img + all_link_soup_script

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

        return dict_output


if __name__ == "__main__":
    url = input("url: ")
    webcrwl = WebCrawler(url, "output25.json", tempo=[0.2, 0.5])
    webcrwl.explore_website()
