from urllib.parse import urlparse


class WebDispatcher:
    def __init__(self, url):
        self.url = urlparse(url)
        self.query = self.url.query

    def get_params(self):
        list_params = []
        for x in self.query.split('&'):
            a, b = x.split('=')
            if b.isdigit():
                type_p = 'int'
            else:
                type_p = 'str'

            list_params.append({'key': a, 'value': b, 'type': type_p})
        return list_params


if __name__ == '__main__':
    wbdisptcher = WebDispatcher(
        "https://www.google.com/search?q=python3+urparse&rlz=12315646&oq=python3+urparse&aqs=chrome..69i57j0i13j0i13i30l4j0i10i13i30j0i13i30j0i10i13i30j0i13i30.3751j0j7&sourceid=chrome&ie=UTF-8")
    print(wbdisptcher.get_params())
