from flask import (Flask, render_template, flash,
                   get_flashed_messages, request, redirect, url_for)
import os
from dotenv import load_dotenv
from page_analyzer.validator import validate_url
from page_analyzer.normalize import get_normalized_url
import psycopg2
from psycopg2.extras import DictCursor
from page_analyzer.time_normalize import get_normalized_time


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/')
def get_index():
    return render_template('index.html')


@app.post('/urls')
def get_add_url():
    url = request.form.get('url')
    errors = validate_url(url)
    if errors:
        flash(errors[0], 'error')
        return render_template('index.html'), 422

    normalized_url = get_normalized_url(url)
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute('SELECT id FROM urls WHERE name = %s', (normalized_url,))
        url_id = curs.fetchone()
        if url_id:
            flash('Страница уже существует', 'warning')
            return redirect(url_for('get_url', id=url_id['id']))

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
    url['created_at'] = get_normalized_time(url['created_at'])
    return render_template('url.html', id=id, **url)


@app.route('/urls')
def get_all_urls():
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute('SELECT * FROM urls')
        urls = curs.fetchall()
    for url in urls:
        url['created_at'] = get_normalized_time(url['created_at'])
    return render_template('all_urls.html', urls=urls)
