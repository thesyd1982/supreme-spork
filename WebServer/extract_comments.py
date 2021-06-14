"""
Script pour Récuperer les commentaire présent dans lHTML et colorer des mots predefinis
TODO :  
-recuperer le js distant
-recuperer les commentaire dans les balise style et dans le css distant
-POO
"""

from bs4 import BeautifulSoup, Comment
import requests
import pprint
import json
from models.colorText import ColorText
from models.webRessource import headers_base as headers

banner_p = '#' * 50 + "ID[{}]" + '#' * 50

y = 0


def parse_HTML_comments(soup):
    global y
    try:
        list_dict = []
        for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
            comment = comment.extract().strip()
            if comment != "":
                y += 1
                dict_comment = {'id': y, 'type': 'HTML', 'text': comment}
                list_dict.append(dict_comment)
        return list_dict
    except Exception as e:
        print("Erreur:" + str(e))


def parse_js_comment(soup):
    global y
    list_dict = []
    for comment in soup.find_all('script'):
        if comment.string:
            for i in comment.string.split('\n'):
                # recuperer commentaire sur une ligne complete
                if i.strip()[:3] == "// ":
                    y += 1
                    dict_comment = {'type': 'JSCL'}
                    dict_comment['id'] = y
                    dict_comment['text'] = i.strip()[3:]
                    list_dict.append(dict_comment)

                # recuperer commentaire sur une ligne
                elif "// " in i.strip():
                    y += 1
                    dict_comment = {'type': 'JSSL'}
                    dict_comment['id'] = y
                    dict_comment['text'] = i.strip().split('//')[1]
                    list_dict.append(dict_comment)

            # recuperer commentaire sur plusieur ligne
            try:
                if "*/" in comment.string.split('/*')[1]:
                    y += 1
                    dict_comment = {'type': 'JSML'}
                    dict_comment['id'] = y
                    dict_comment['text'] = comment.string.split('/*')[1].split('*/')[0]
                    list_dict.append(dict_comment)
            except Exception as e:
                pass
    return list_dict


def get_all_comments(url, dict_word=None, json_path=None):
    soup = BeautifulSoup(requests.get(url, headers=headers).content, 'lxml')
    htmlcoms = parse_HTML_comments(soup)
    jscoms = parse_js_comment(soup)
    y = len(htmlcoms)+len(jscoms)
    dict_final = {'URL': url, 'countResults': y, 'commentsList': htmlcoms + jscoms}
    if json_path:
        with open(json_path, 'w') as outfile:
            json.dump(dict_final, outfile)
        return json.dumps(dict_final)

    p = ColorText(pprint.pformat(dict_final))
    print(p.color_words({('config','monitoring'):'red'}))



if __name__ == "__main__":
    get_all_comments("https://www.nike.com/fr/t/chaussure-air-jordan-1-mid-scZZ99/554724-133")
