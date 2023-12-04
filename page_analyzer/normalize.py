from urllib.parse import urlparse


def get_normalized_url(url):
    normalized_url = urlparse(url)
    result = f"{normalized_url.scheme}://{normalized_url.netloc}"
    return result