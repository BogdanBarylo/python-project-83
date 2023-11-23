from flask import Flask, render_template, flash, get_flashed_messages, request, redirect, url_for
import os
from dotenv import load_dotenv
from page_analyzer.validator import get_validate
from page_analyzer.normalize import get_normalize_url
import datetime
import psycopg2


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


@app.route('/')
def index():
    return render_template ('index.html')
    
@app.post('/urls')
def get_add_url():
    url = request.form.get('url')
    errors = get_validate(url)
    if errors:
        return render_template('index.html', errors = errors), 422
    
    normalize_url = get_normalize_url(url)
    current_date = datetime.datetime.now().date()
    with conn.cursor() as curs:
        curs.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s)',
                     (normalize_url, current_date))
        curs.connection.commit() 
        curs.execute('SELECT id FROM urls WHERE name = %s', (normalize_url))
        dict_curs = curs.fetchone()
    url_id = dict_curs['id']
    return redirect(url_for('get_url', id = url_id))
    

@app.get('/url/<int:id>')
def get_url(id):
    with conn.cursor() as curs:
        curs.execute('SELECT name, created_at FROM urls WHERE name = %s', (id))
        dict_curs = curs.fetchone()
    name = dict_curs['name']
    date = dict_curs['created_at']
    return render_template ('url.html', id = id, name = name, date = date)    


@app.route('/urls')
def get_all_urls():
    with conn.cursor() as curs:
        curs.execute('SELECT * FROM urls;')
        dict_curs = curs.fetchone()
    return render_template('all_urls.html', urls = dict_curs)



