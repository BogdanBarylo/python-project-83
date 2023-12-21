
"""
структура теста:
1. подготовить данные (опционально), точный термин: setup
2. выполнить тестируемое действие
3. assert
4. очистить данные (опционально), точный термин: teardown

фикстура pytest – переиспользуемый компонент для выполнения setup + teardown
"""

from page_analyzer.db import clear_db, insert_url
from pytest import fixture


@fixture
def truncate_db():
    yield
    clear_db()


@fixture
def testing_url():
    return 'https://example.com'


@fixture
def add_url(testing_url):
    yield str(insert_url(testing_url)['id'])
