from flask import Flask, render_template, flash, request, redirect, url_for
import os
from dotenv import load_dotenv
from page_analyzer.validator import validate_url
from page_analyzer.normalize import get_normalized_url
import psycopg2
from psycopg2.extras import DictCursor
from page_analyzer.time_normalize import change_format_time
import requests
from page_analyzer.soap import get_tags


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def get_error(error):
    return render_template('500.html'), 500


@app.route('/')
def get_index():
    return render_template('index.html')


@app.post('/urls')
def add_url():
    url = request.form.get('url')
    errors = validate_url(url)
    if errors:
        flash(errors[0], 'error')
        return render_template('index.html'), 422

    normalized_url = get_normalized_url(url)
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute('SELECT id FROM urls WHERE name = %s', (normalized_url,))
        id = curs.fetchone()
        if id:
            flash('Страница уже существует', 'warning')
            return redirect(url_for('get_url', id=id['id']))

        curs.execute('INSERT INTO urls (name) VALUES (%s) RETURNING id',
                     (normalized_url,))
        url_id = curs.fetchone()
        curs.connection.commit()
        flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url', id=url_id['id']))


@app.get('/url/<int:id>')
def get_url(id):
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute('SELECT name, created_at FROM urls WHERE id = %s', (id,))
        url = curs.fetchone()
    if not url['name'] or not url['created_at']:
        return redirect(url_for('page_not_found'))
    url['created_at'] = change_format_time(url['created_at'])
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute('''SELECT id, created_at,
                     status_code, h1, title,
                     description
                     FROM url_checks
                     WHERE url_id = %s
                     ORDER BY id DESC''', (id,))
        checks = curs.fetchall()
        for check in checks:
            check['created_at'] = change_format_time(check['created_at'])
    return render_template('url.html', id=id, checks=checks, **url)


@app.route('/urls')
def get_all_urls():
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute('''SELECT urls.id, urls.name,
                     urls.created_at, url_checks.status_code,
                     MAX(url_checks.created_at) AS last_checked_at
                     FROM urls
                     LEFT JOIN url_checks
                     ON urls.id = url_checks.url_id
                     GROUP BY urls.id, urls.name, urls.created_at,
                     url_checks.status_code
                     ORDER BY urls.id DESC''')
        urls = curs.fetchall()
    for url in urls:
        url['last_checked_at'] = change_format_time(url['last_checked_at'])
    return render_template('all_urls.html', urls=urls)


@app.post('/urls/<int:id>/checks')
def add_url_check(id):
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute('SELECT name FROM urls WHERE id = %s', (id,))
        name = curs.fetchone()
    response = requests.get(name[0])
    try:
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'error')
        return redirect(url_for('get_url', id=id))
    status_code = response.status_code
    tags_dict = get_tags(response)

    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute('''INSERT INTO url_checks
                     (url_id, status_code, h1, title, description)
                     VALUES (%s, %s, %s, %s, %s)''',
                     (id, status_code, tags_dict['h1'],
                      tags_dict['title'], tags_dict['description']))
        curs.connection.commit()
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_url', id=id))
