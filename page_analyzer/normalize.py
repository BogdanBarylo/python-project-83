from urllib.parse import urlparse


def get_normalized_url(url):
    normalized_url = urlparse(url)
    result = f"{normalized_url.scheme}://{normalized_url.netloc}"
    return result


def datetime_to_str(date):
    if date is None:
        return ''
    only_date = date.date()
    date_string = only_date.strftime('%Y-%m-%d')
    return date_string
