import pytest
import re
from page_analyzer import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_add_url_success(client):
    response = client.post('/urls', data={'url': 'https://agroex.ru/'})
    url_pattern = re.compile(r'^https?://(?:www\.)?([a-zA-Z0-9-]+)(?:\.[a-zA-Z]+)+/?$')
    assert url_pattern.match('https://agroex.ru/'), "Invalid URL format"
    assert response.status_code == 302
