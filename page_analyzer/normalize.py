from urllib.parse import urlparse


def get_normalized_url(url):
    normalized_url = urlparse(url)
    result = "{}://{}".format(normalized_url.scheme, normalized_url.netloc)
    return result
