from flask import Flask, render_template, flash, request, redirect, url_for
import os
from dotenv import load_dotenv
from page_analyzer.validator import validate_url
from page_analyzer.normalize import get_normalized_url
from page_analyzer.time_normalize import change_format_time
import requests
from page_analyzer.soap import get_tags
from page_analyzer.db_methods import (get_id_urls, insert_name_urls,
                                      get_name_and_date_urls, get_checks,
                                      get_all_information, get_name_urls,
                                      insert_check_url_checks)


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
    id = get_id_urls(normalized_url)
    if id:
        flash('Страница уже существует', 'warning')
        return redirect(url_for('get_url', id=id['id']))
    url_id = insert_name_urls(normalized_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url', id=url_id['id']))


@app.get('/url/<id>')
def get_url(id):
    url = get_name_and_date_urls(id)
    if not url['name'] or not url['created_at']:
        return redirect(url_for('page_not_found'))
    url['created_at'] = change_format_time(url['created_at'])
    checks = get_checks(id)
    for check in checks:
        check['created_at'] = change_format_time(check['created_at'])
    return render_template('url.html', id=id, checks=checks, **url)


@app.get('/urls')
def get_all_urls():
    urls = get_all_information()
    for url in urls:
        url['last_checked_at'] = change_format_time(url['last_checked_at'])
    return render_template('all_urls.html', urls=urls)


@app.post('/urls/<id>/checks')
def add_url_check(id):
    name = get_name_urls(id)
    try:
        response = requests.get(name[0])
        response.raise_for_status()
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'error')
        return redirect(url_for('get_url', id=id))
    status_code = response.status_code
    tags_dict = get_tags(response)
    insert_check_url_checks(id, status_code, tags_dict)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_url', id=id))
