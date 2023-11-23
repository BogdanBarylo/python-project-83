from urllib.parse import urlparse, urljoin

def get_normalize_url(url):
    normalize_url = urlparse(url)
    result = urljoin(normalize_url.scheme, normalize_url.netloc)
    return result
