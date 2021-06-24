from urllib.parse import urlparse

headers_base = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}


class URL:
    def __init__(self, url, referrer_url=None):
        self.url = url
        self.referrer_url = referrer_url
        self.absolute = None
        self.set_absolute()

        self.scheme = None
        self.subdomain = None

        self.domain_pur = None
        self.current_path = None
        self.parent_path = None
        self.root_path = None

        if self.absolute:
            self.set_info_url(self.url)
            self.real_loc = url

        else:
            self.set_info_url(self.referrer_url)
            self.real_loc = self.get_absolute()

    def set_absolute(self):
        if self.url[:2] != "//" and self.url[:7] != "http://" and self.url[:8] != "https://":
            self.absolute = False
        else:
            self.absolute = True

    def set_info_url(self, url):
        url = urlparse(url)
        self.scheme = url.scheme

        # Test si il y a un sous domaine
        if url.hostname.count(".") > 1:
            self.subdomain = url.hostname.split('.')[0]
            self.domain_pur = ".".join(url.hostname.split('.')[1:])
        else:
            self.domain_pur = url.hostname

        # Verifier si il y a parent path et current path
        self.current_path = "/".join((self.scheme + "://" + url.hostname + url.path).split('/')[:-1]) + "/"
        self.root_path = self.scheme + "://" + url.hostname + "/"
        if url.path.count('/') > 0:
            self.parent_path = self.scheme + "://" + url.hostname + "/".join(url.path.split("/")[:-2]) + "/"

    def get_absolute(self):
        if self.url[:1] == "/":
            return self.root_path + self.url[1:]
        elif self.url[:2] == "./":
            return self.current_path + self.url[2:]
        elif self.url[:3] == "../":
            return self.parent_path + self.url[3:]
        elif self.url[:1] == "#":
            return self.referrer_url + self.url
        else:
            return self.referrer_url + self.url


if __name__ == "__main__":
    url1 = URL("#chemin/vers/monfichier.html", "http://www.exemple.com:80/chemin/vers/monfichier.html")
    print(url1.domain_pur)
    print(url1.current_path)
    print(url1.parent_path)
    print(url1.root_path)
    print(url1.real_loc)
