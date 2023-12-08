# import pytest
# import re
# from page_analyzer import app


# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     with app.test_client() as client:
#         yield client


# def test_add_url_success(client):
#     response = client.post('/urls', data={'url': 'https://agroex.ru/'})
    
#     assert response.status_code == 302

#     expected_bytes = 'Страница успешно добавлена'.encode('utf-8')
#     assert expected_bytes in response.data
