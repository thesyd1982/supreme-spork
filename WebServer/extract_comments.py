"""
Script pour Récuperer les commentaire présent dans lHTML et colorer des mots predefinis
TODO :  
-Recuperer les commentaire JS 
-Faire une wordlist de mot a colorer
-exporter en json {'nmbreResult':3,'commentList':[{'id':1,'text';'dssdsdds'},{'id':2,'text';'sdffsfs'}]}
-verifier si lurl est correct 
-except et print les erreur
"""
from bs4 import BeautifulSoup, Comment
import requests
from termcolor import colored

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}
banner_p = '#' * 50 + "ID[{}]" + '#' * 50


# Syntax Color for
def color_text(listWord, text):
    for word in listWord:
        text = text.replace(word, colored(word, 'red'))
    return text


def get_HTML_comments(url, hitWordList):
    result = ""
    y = 0
    soup = BeautifulSoup(requests.get(url, headers=headers).content, 'lxml')
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        comment = comment.extract().strip()
        if comment != "":
            y += 1
            result += banner_p.format(y) + "\n\n" + color_text(hitWordList, comment) + "\n\n"
    return result


if __name__ == "__main__":
    hitWordList = ['email', 'password', 'id']
    url = "https://www.nike.com/fr/t/chaussure-air-jordan-1-mid-scZZ99/554724-133"
    print(get_HTML_comments(url, hitWordList))
