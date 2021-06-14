"""
Script pour Récuperer les commentaire présent dans lHTML et colorer des mots predefinis
TODO :  
-Recuperer les commentaire JS 
"""
from bs4 import BeautifulSoup, Comment
import requests
import json
from models.colorText import ColorText

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}
banner_p = '#' * 50 + "ID[{}]" + '#' * 50


def get_HTML_comments(url, dict_word, json_path=None):
    try:
        list_dict = []
        result = ""
        y = 0
        soup = BeautifulSoup(requests.get(url, headers=headers).content, 'lxml')
        for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
            comment = comment.extract().strip()
            if comment != "":
                p = ColorText(comment)
                y += 1
                dict_comment = {'id': y, 'text': comment}
                list_dict.append(dict_comment)
                result += banner_p.format(y) + "\n\n" + p.color_words(dict_word) + "\n\n"

    except Exception as e:
        print("Erreur:" + str(e))
    dict_final = {'countResults': y, 'commentsList': list_dict}
    if json_path:
        with open(json_path, 'w') as outfile:
            json.dump(dict_final, outfile)
        return json.dumps(dict_final)
    return result


if __name__ == "__main__":
    hitWordList = {('client', 'password', 'id'): 'blue'}
    url = "https://www.nike.com/fr/t/chaussure-air-jordan-1-mid-scZZ99/554724-133"
    print(get_HTML_comments(url, hitWordList, 'result.json'))
