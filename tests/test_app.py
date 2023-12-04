import pytest
from page_analyzer.app import add_url


def test_add_url_successful(client):
    response = client.post('/urls', data={'url': 'https://agroex.ru/'}, follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction() as sess:
        #assert b'Страница успешно добавлена' in sess['_flashes'][0][1]
        #assert sess['_flashes'][0][0] == 'success'
        pass
