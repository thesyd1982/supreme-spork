"""
Simple Scraper
TODO:
-recuperer les dossier et les tester sans suffix
"""
import random
import requests
from queue import Queue
import time
from models.webRessource import headers_base as headers
from bs4 import BeautifulSoup


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


def explore_website(url_base, path_output=None, verbose=True, error_limit=10, tempo=[0.5, 1.5]):
    # Initaliser la Queue
    q = Queue()
    # Ajouter l'URL de base
    q.put(url_base)

    result = []
    error = 0
    erreur_total = 0

    domain_base, path_base = get_default_domain_and_path(url_base)

    s = requests.Session()
    s.headers.update(headers)

    tempo = random.uniform(tempo[0], tempo[1])

    # Tant que la liste d'url a crawler n'est pas vide
    while not q.empty():
        # Remettre par defaut les variables
        soup = None
        all_link = []

        # récuperer la prochaine url
        url_now = q.get()

        # Essayer de recupérer le contenu de la page
        try:
            soup = BeautifulSoup(s.get(url_now, headers=headers).content, 'lxml')
            error = 0
        except:
            error += 1
            erreur_total += 1

        # Si il y a un contenu
        if soup:
            # recuperer toutes les balise de liens
            all_link_soup_a = [{'attr': 'href', 'object': x} for x in soup.find_all('a')]
            all_link_soup_link = [{'attr': 'href', 'object': x} for x in soup.find_all('link')]
            all_link_soup_meta = [{'attr': 'content', 'object': x} for x in soup.find_all('meta')]
            all_link_soup_img = [{'attr': 'src', 'object': x} for x in soup.find_all('img')]
            all_link_soup_script = [{'attr': 'src', 'object': x} for x in soup.find_all('script')]
            all_link_soup = all_link_soup_a + all_link_soup_link + all_link_soup_meta + all_link_soup_img + all_link_soup_script

            # Trier les liens recuperer
            for y in all_link_soup:
                try:
                    x = y['object'][y['attr']]
                    if x[:1] == "/":
                        if x[:2] == "//":
                            x = x[1:]
                        if path_base + x not in result:
                            # Ajouter au résultat final
                            result.append(path_base + x)
                            # Ajouter pour les prochaines requete
                            if y['attr'] == 'href':
                                q.put(path_base + x)

                    elif domain_base in get_default_domain_and_path(x)[0]:
                        if x not in result:
                            # Ajouter au résultat final
                            result.append(x)
                            # Ajouter pour les prochaines requete
                            if y['attr'] == 'href':
                                q.put(x)
                except:
                    pass

            # Affichage
            if verbose:
                print('#' * 100)
                print(url_now)
                print('result length')
                print(len(result))
                print('queue lenght')
                print(q.qsize())
                print('error')
                print(error)
            time.sleep(tempo)
            if error > error_limit:
                print(" + ] Nombre d'erreur limite atteinte")
                break

    # Fermer la session
    s.close()

    # Trier par ordre alphabetique
    result.sort()

    # Output file
    if path_output:
        with open(path_output, 'w') as outputFile:
            outputFile.write('URL BASE : ' + url_base + "\n")
            outputFile.write('Nbr Résultat : ' + str(len(result)) + "\n")
            outputFile.write('Erreur : ' + str(erreur_total) + "\n")

            for x in result:
                outputFile.write(x + '\n')
    return result


if __name__ == "__main__":
    explore_website("http://www.miel-de-corse.fr/boutique/", "output.txt")
