from bs4 import BeautifulSoup


def get_tags(response):
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    soup_dict = {'h1': get_parse_h1(soup),
                 'title': get_parse_title_tag(soup),
                 'description': get_parse_content(soup)}
    return soup_dict


def get_parse_h1(soup):
    h1_tag = soup.find('h1')
    if not h1_tag:
        return ''
    h1_content = h1_tag.text.strip()
    return h1_content


def get_parse_title_tag(soup):
    title_tag = soup.find('title')
    if not title_tag:
        return ''
    title_content = title_tag.text.strip()
    return title_content


def get_parse_content(soup):
    meta_description = soup.find('meta', {'name': 'description'})
    if not meta_description and 'content' in meta_description.attrs:
        return ''
    content = meta_description['content']
    return content
