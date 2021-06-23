"""TODO
Ecrire un paquet de tools
Ecrire un outil XSS
Ecrire un README avec https://github.com/RichardLitt/standard-readme/blob/master/README.md
Completer touts les script avec PayloadAllTheThing pour ajouter des payloads a chaque exploit
Rassembler toutes les LFI dans une classe / pareil pour les RFI
-Faire un analyser pour le dispatcher (analyser l'url, la page, recuperer des forms, ect...) (en sortie une liste de dictionnaire avec {'url':url,'exploit':['XSS','LFI','PHP_ASSERT']}
-Faire un dispatcher pour le crawler



"""
notes = """
NOTES
Chemin absolue == htrtps://sdfsdfsdf.com/sdfdsflkdsf.php?id=qdqsd
Chemin relatif ==



parse les port si il y a
http = protocole
www.exemple.com
www = sous-domaine
exemple  = nom de domaine de deuxieme niveau
com = nom de domaine de premier niveau


données d’authentification (optionnelles, le service peut les demander séparément de façon plus sécurisée que via l’URL) :
Jojo : nom d’utilisateur, notamment utile pour accéder à des parties non publiques d'un site web,
: : caractère de séparation si un mot de passe est indiqué,
lApIn : mot de passe de l'utilisateur, indiqué ici « en clair »,
@ : caractère terminant les données d'identification présentes avant le nom du service.

: : caractère indiquant qu’un numéro de port est précisé en suffixe,
8888 : numéro de port TCP/IP du serveur HTTP, doit être précisé lorsqu’il ne s’agit pas du port standard pour le protocole utilisé (qui est 80 pour HTTP, 21 pour FTP…),
[2001:db8::1234]:8888 : Dans le cas d'une adresse IPv6, si on veut spécifier le port, il est obligatoire de mettre l'adresse entre crochets pour ne pas confondre le port et l'adresse.

? : caractère de séparation obligatoire pour indiquer que des données complémentaires suivent.
q=req&q2=req2 - chaîne de requête, traitée par la page web sur le serveur.

# : caractère de séparation obligatoire pour indiquer un signet ou une balise,
signet : identificateur du signet ou de la balise. Il s’agit d’un emplacement à l’intérieur de la page web retournée par le service, cette donnée sera traitée par le navigateur web.

./ correspond au dossier actuel ;
../ correspond au dossier parent ;
/ correspond au dossier racine.

exemple pour parse
http://www.exemple.com:80/chemin/vers/monfichier.html?clé1=valeur1&clé2=valeur2#QuelquePartDansLeDocument


URL ACTUEL
Recuperer :
PROTOCOL
SOUS DOMAINE
NOM DE DOMAIN NIV 2
LE NOM E DOMAINE NIV 1
LE PORT
avec ca fabriquer l url racine

URL PARSE DANS LA PAGE
1 tri url absolue ou relatif

si commence par http ou par // == url absolue sinon url relatif


AVANT TOUT 
ne doit pas non plus etre vide ni commencer par javascript:

ABSOLUE
commencant par http 
commence par // ajouter le protocole de lurl actuel plus un seprateur
l' ajouter

RELATIF
commencant par / = url racine + url_parse
commencant par ./ = dossier actuelle de lurl actuelle + url_parse
commencant par ../ = dossier parent de lurl actuelle + url_parse
commencant par # = url_courante + chemin
sinon url actuelle + / + url_parse



Creer un objet url qui contiendra tous ses attribut et methode
"""