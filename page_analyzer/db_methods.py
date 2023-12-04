from psycopg2.extras import DictCursor
from dotenv import load_dotenv
import os
import psycopg2


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')



def open_db(func):
    def wrapper(*args, **kwargs):
        conn = psycopg2.connect(DATABASE_URL)
        with conn:
                with conn.cursor(cursor_factory=DictCursor) as curs:
                    return func(curs, *args, **kwargs)
    return wrapper


@open_db
def get_id_urls(curs, url):
    curs.execute('SELECT id FROM urls WHERE name = %s', (url,))
    return curs.fetchone()


@open_db
def insert_name_urls(curs, url):
    curs.execute('INSERT INTO urls (name) VALUES (%s) RETURNING id',
                 (url,))
    url_id = curs.fetchone()
    curs.connection.commit()
    return url_id


@open_db
def get_name_and_date_urls(curs, id):
    curs.execute('SELECT name, created_at FROM urls WHERE id = %s', (id,))
    return curs.fetchone()


@open_db
def get_checks(curs, id):
    curs.execute('''SELECT id, created_at,
                    status_code, h1, title,
                    description
                    FROM url_checks
                    WHERE url_id = %s
                    ORDER BY id DESC''', (id,))
    return curs.fetchall()


@open_db
def get_all_information(curs):
    curs.execute('''SELECT urls.id, urls.name,
                     urls.created_at, url_checks.status_code,
                     MAX(url_checks.created_at) AS last_checked_at
                     FROM urls
                     LEFT JOIN url_checks
                     ON urls.id = url_checks.url_id
                     GROUP BY urls.id, urls.name, urls.created_at,
                     url_checks.status_code
                     ORDER BY urls.id DESC''')
    return curs.fetchall()


@open_db
def get_name_urls(curs, id):
    curs.execute('SELECT name FROM urls WHERE id = %s', (id,))
    return curs.fetchone()


@open_db
def insert_check_url_checks(curs, id, status_code, tags_dict):
    curs.execute('''INSERT INTO url_checks
                 (url_id, status_code, h1, title, description)
                 VALUES (%s, %s, %s, %s, %s)''',
                 (id, status_code, tags_dict['h1'],
                  tags_dict['title'], tags_dict['description']))
    curs.connection.commit()
