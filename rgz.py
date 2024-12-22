from flask import Blueprint, render_template, request, redirect, session, url_for, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import json

rgz = Blueprint('rgz', __name__)

users = {}

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='repuyk_kate_knowledge_base1',
            user='repuyk_kate_knowledge_base1',
            password='1234'
        )
        cur = conn.cursor(cursor_factory= RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "dabase.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@rgz.route('/rgz')
def rgzz():
    return render_template('rgz/rgz.html')

@rgz.route('/registers', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        response = jsonrpc_register(login, password)
        
        if response['result']:
            return redirect(url_for('rgz.rgzz'))
        else:
            return render_template('rgz/registers.html', error=response['error'])
    
    return render_template('rgz/registers.html')

def jsonrpc_register(login: str, password: str):
    if login in users:
        return {'result': False, 'error': 'Пользователь с таким логином уже существует'}
    
    users[login] = password
    return {'result': True, 'error': None}


@rgz.route('/logins', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        
        response = jsonrpc_login(login, password)
        
        if response['result']:
            session['user'] = login
            return redirect(url_for('rgz.rgzz'))
        else:
            return render_template('rgz/logins.html', error=response['error'])
    
    return render_template('rgz/logins.html')

def jsonrpc_register(login: str, password: str):
    if login in users:
        return {'result': False, 'error': 'Пользователь с таким логином уже существует'}
    
    users[login] = password
    return {'result': True, 'error': None}

def jsonrpc_login(login: str, password: str):
    if login not in users or users[login] != password:
        return {'result': False, 'error': 'Неверный логин или пароль'}
    
    return {'result': True, 'error': None}

@rgz.route('/api/jsonrpc', methods=['POST'])
def jsonrpc():
    data = request.get_json()
    method = data.get('method')
    params = data.get('params')
    
    if method == 'register':
        response = jsonrpc_register(params['login'], params['password'])
    elif method == 'login':
        response = jsonrpc_login(params['login'], params['password'])
    else:
        response = {'result': None, 'error': 'Метод не найден'}
    
    return jsonify(response)