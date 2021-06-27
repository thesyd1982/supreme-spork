from urllib.parse import urlparse

headers_base = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}

headers_crawler = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}


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
        self.is_special = False
        self.is_anchor = False
        self.is_js = False

        if self.absolute:
            self.set_info_url(self.url)
            self.real_loc = url

        else:
            self.set_info_url(self.referrer_url)
            self.real_loc = self.get_absolute()
            if not self.is_special:
                self.set_info_url(self.real_loc)


    def set_absolute(self):
        if self.url[:2] == "//":
            self.set_info_url(self.referrer_url)
            self.url = self.scheme + self.url
            self.absolute = True
        elif self.url[:7] == "http://" or self.url[:8] == "https://":
            self.absolute = True

        else:
            self.absolute = False

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
        self.root_path = self.scheme + "://" + url.hostname + "/"
        if self.scheme + "://" + url.hostname + url.path != self.root_path:
            self.current_path = "/".join((self.scheme + "://" + url.hostname + url.path).split('/')[:-1]) + "/"
        else:
            self.current_path = self.root_path
        if url.path.count('/') > 0:
            self.parent_path = self.scheme + "://" + url.hostname + "/".join(url.path.split("/")[:-2]) + "/"

    def get_absolute(self):
        self.url = self.url.replace('\\', '/')
        if self.url[:1] == "/":
            return self.root_path + self.url[1:]
        elif self.url[:2] == "./":
            return self.current_path + self.url[2:]
        elif self.url[:3] == "../":
            return self.parent_path + self.url[3:]
        elif self.url[:1] == "#":
            self.is_anchor = True
            if "#" in self.referrer_url:
                return self.referrer_url
            else:
                return self.referrer_url + self.url
        elif self.url[:7] == "mailto:" or self.url[:4] == "tel:":
            self.is_special = True
            return self.url
        elif self.url[:11] == "javascript:":
            self.is_js = True
        else:
            if self.referrer_url[-1:] == "/":
                return self.referrer_url + self.url
            else:
                return self.current_path + self.url


if __name__ == "__main__":
    url1 = URL("chemin.html", "http://www.exemple.com:80/chemin/")
    print(url1.domain_pur)
    print(url1.current_path)
    print(url1.parent_path)
    print(url1.root_path)
    print(url1.real_loc)
