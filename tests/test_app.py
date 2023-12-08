from flask.testing import FlaskClient
import pytest
import re
from page_analyzer import app
# from page_analyzer.db import del_url


TEST_URL = 'https://example.com'


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_add_url_success(client: FlaskClient):
    response = client.post('/urls', data={'url': TEST_URL})
    assert response.status_code == 302
    redirected_response = client.get(response.location, follow_redirects=True)
    assert redirected_response.status_code == 200
    flash = r'Страница успешно добавлена'
    assert re.search(flash, redirected_response.data.decode()) is not None


def test_add_existing_url(client: FlaskClient):
    response = client.post('/urls', data={'url': TEST_URL})
    assert response.status_code == 302
    redirected_response = client.get(response.location, follow_redirects=True)
    assert redirected_response.status_code == 200
    flash = r'Страница уже существует'
    assert re.search(flash, redirected_response.data.decode()) is not None


def test_invalid_url(client: FlaskClient):
    response = client.post('/urls', data={'url': 'invalid-url'})
    assert response.status_code == 422
    assert re.search(r'Некорректный URL', response.data.decode())


def test_get_existing_url(client):
    response = client.get('/urls/1')
    assert response.status_code == 200
    assert re.search(r'Сайт:', response.data.decode())


def test_get_nonexistent_url(client):
    response = client.get('/urls/100')
    assert response.status_code == 404


def test_get_all_urls(client):
    response = client.get('/urls')
    assert response.status_code == 200
    assert re.search(r'Сайты', response.data.decode())


def test_add_check(client):
    response = client.post('/urls/1/checks', data={'url': TEST_URL})
    assert response.status_code == 302
    redirected_response = client.get(response.location, follow_redirects=True)
    assert redirected_response.status_code == 200
    flash = r'Страница успешно проверена'
    assert re.search(flash, redirected_response.data.decode()) is not None
