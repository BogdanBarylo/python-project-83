from bs4 import BeautifulSoup


def get_parse(responce):
    html_content = responce.text
    soup = BeautifulSoup(html_content, 'html.parser')
    soup_dict = {'h1': get_parse_h1(soup),
                 'title': get_parse_title_tag(soup),
                 'description': get_parse_content(soup)}
    return soup_dict


def get_parse_h1(soup):
    h1_tag = soup.find('h1')
    if h1_tag:
        h1_content = h1_tag.text.strip()
        return h1_content
    else:
        return None


def get_parse_title_tag(soup):
    title_tag = soup.find('title')
    if title_tag:
        title_content = title_tag.text.strip()
        return title_content
    else:
        return None


def get_parse_content(soup):
    meta_description = soup.find('meta', {'name': 'description'})
    if meta_description and 'content' in meta_description.attrs:
        content = meta_description['content']
        return content
    else:
        return None
