from flask import Flask, render_template, flash, request, redirect, url_for
import os
from dotenv import load_dotenv
from page_analyzer.validator import validate_url
from page_analyzer.normalize import get_normalized_url, datetime_to_str
import requests
from page_analyzer.parse_head import get_tags
from page_analyzer.db import (get_url_id, insert_url,
                              get_url_by_id, get_checks,
                              get_urls, insert_check)


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def get_error(error):
    return render_template('500.html'), 500


@app.get('/')
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
    id = get_url_id(normalized_url)
    if id:
        flash('Страница уже существует', 'warning')
        return redirect(url_for('get_url', id=id['id']))
    url_id = insert_url(normalized_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url', id=url_id['id']))


@app.get('/urls/<int:id>')
def get_url(id):
    url = get_url_by_id(id)
    if not url:
        return render_template('404.html'), 404
    url['created_at'] = datetime_to_str(url['created_at'])
    checks = get_checks(id)
    for check in checks:
        check['created_at'] = datetime_to_str(check['created_at'])
    return render_template('url.html', id=id, checks=checks, **url)


@app.get('/urls')
def get_all_urls():
    urls = get_urls()
    for url in urls:
        url['last_checked_at'] = datetime_to_str(url['last_checked_at'])
    return render_template('all_urls.html', urls=urls)


@app.post('/urls/<int:id>/checks')
def add_url_check(id):
    name = get_url_by_id(id)
    try:
        response = requests.get(name[0])
        response.raise_for_status()
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'error')
        return redirect(url_for('get_url', id=id))
    status_code = response.status_code
    tags_dict = get_tags(response)
    insert_check(id, status_code, tags_dict)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_url', id=id))
