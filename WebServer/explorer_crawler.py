"""
Simple Crawler
TODO:
-recuperer les dossier et les tester sans suffix
-rajouter le status de la requete dans le result
-mulithread ?
-liste en entree
"""
import random
import requests
from queue import Queue
import time
from models.webRessource import headers_base as headers
from models.timePrint import print_timep
from models.outputFile import save_json
from bs4 import BeautifulSoup


# Récuperer le domaine et le path de base
def get_default_domain_and_path(url):
    prefix, domain = url.split('//')
    path = prefix + "//"
    if '/' in domain:
        domain = domain.split('/')[0]
    if "www." in domain:
        domain = domain.replace('www.', '')
        path += "www."
    path += domain
    return domain, path


def explore_website(url_base, path_output=None, verbose=True, error_limit=10, tempo=None):
    # Initaliser la Queue
    q = Queue()
    # Ajouter l'URL de base
    q.put(url_base)
    result = []
    error, erreur_total, nbr_requete = 0, 0, 0

    # Récuperer le domaine de base et le chemin par defaut
    domain_base, path_base = get_default_domain_and_path(url_base)

    # Init la session
    s = requests.Session()
    s.headers.update(headers)

    # Init Tempo
    if tempo:
        print('[ * ] Tempo : {} s - {} s'.format(tempo[0], tempo[1]))
        tempo = random.uniform(tempo[0], tempo[1])

    else:
        tempo = [1, 2]
        print('[ * ] Default tempo {} s - {} s'.format(tempo[0], tempo[1]))

    # Calcul du temps
    time_start = time.time()

    # Tant que la liste d'url a crawler n'est pas vide
    while not q.empty():
        # Remettre par defaut les variables
        soup = None

        # récuperer la prochaine url
        url_now = q.get()

        # Essayer de recupérer le contenu de la page
        try:
            soup = BeautifulSoup(s.get(url_now, headers=headers).content, 'lxml')
            nbr_requete += 1
            error = 0
        except:
            error += 1
            erreur_total += 1

        # Si il y a un contenu
        if soup:
            # recuperer toutes les balise de liens
            all_link_soup_a = [{'attr': 'href', 'object': x} for x in soup.find_all('a')]
            all_link_soup_link = [{'attr': 'href', 'object': x} for x in soup.find_all('link')]
            #all_link_soup_meta = [{'attr': 'content', 'object': x} for x in soup.find_all('meta')]
            all_link_soup_img = [{'attr': 'src', 'object': x} for x in soup.find_all('img')]
            all_link_soup_script = [{'attr': 'src', 'object': x} for x in soup.find_all('script')]
            all_link_soup = all_link_soup_a + all_link_soup_link + all_link_soup_img + all_link_soup_script

            # Trier les liens recuperer
            for y in all_link_soup:
                try:
                    x = y['object'][y['attr']]
                    try:
                        urlnow_domain = get_default_domain_and_path(x)[0]
                    except:
                        urlnow_domain = False

                    if x[:1] == "/":
                        if x[:2] == "//":
                            x = x[1:]
                        if path_base + x not in result:
                            # Ajouter a la liste des résultats
                            result.append(path_base + x)
                            # Ajouter dans la queue
                            if y['attr'] == 'href':
                                q.put(path_base + x)
                    elif urlnow_domain:
                        if domain_base in urlnow_domain:
                            if x not in result:
                                # Ajouter a la liste des résultats
                                result.append(x)
                                # Ajouter dans la queue
                                if y['attr'] == 'href':
                                    q.put(x)

                    elif x[:4] != "http":
                        uri = "/".join(url_now.split('/')[:-1]) + "/"
                        urx = uri + x
                        if urx not in result:
                            result.append(urx)
                            if y['attr'] == 'href':
                                q.put(urx)
                except Exception as e:
                    pass

            # Affichage
            if verbose:
                print('#' * 100)
                print('URL en cours : {}'.format(url_now))
                print('Nombre de requete : {}'.format(nbr_requete))
                print('Nombre de résultat : {}'.format(len(result)))
                print('Nombre de requetes restantes : {}'.format(q.qsize()))
                print("Nombre d'erreur consecutives : {}".format(error))
                print("Nombre d'erreur total : {}".format(erreur_total))
                print("Temps : {}".format(print_timep(int(time.time() - time_start))))
            time.sleep(tempo)
            if error > error_limit:
                print(" + ] Nombre d'erreur limite atteinte")
                break

    # Fermer la session
    s.close()

    # Trier les résultats
    result.sort()

    # Output Format
    dict_output = {'url_base': url_base,
                   'req_count': nbr_requete,
                   'res_count': len(result),
                   'err_count': erreur_total,
                   'crawl_time': round(time.time() - time_start, 2),
                   'result': result}
    # Output file
    if path_output:
        save_json(path_output, dict_output)

    return dict_output


if __name__ == "__main__":
    url = input("url: ")
    domain_base, path_base = get_default_domain_and_path(url)
    explore_website(url, "output" + domain_base.split(".")[0] + ".json", tempo=[0.2,0.4 ])
