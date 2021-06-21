headers_base = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}


# Récuperer le domaine et le path de base
def get_default_domain_and_path(url):
    prefix, domain = url.split('//')
    path = prefix + "//"
    if '/' in domain:
        domain = domain.split('/')[0]
    if "www." in domain:
        domain = domain.replace('www.', '')
        path += "www."
    path += domain
    return domain, path
