from flask import Flask, request, jsonify, render_template, redirect, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
from traitlets import This
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import jwt
from os import path
from functools import wraps
from datetime import datetime, timedelta


SECRET_KEY = '040520240600'

app = Flask(__name__)

app.config.update({
    'DB_TYPE': 'postgres',  
    'DB_HOST': '127.0.0.1',
    'DB_NAME': 'rgz',
    'DB_USER': 'rgz',
    'DB_PASSWORD': '123',
    'DB_PORT': 5432, 
})


@app.route('/') 


@app.route('/rgz')
def rgzz():
    return render_template('rgz/rgz.html')


@app.route('/registers')
def registers():
    return render_template('rgz/registers.html')


@app.route('/logins')
def logins():
    return render_template('rgz/logins.html')


@app.route('/api', methods=['POST'])
def api_alias():
    return api() 



def generate_token(username):
    token = jwt.encode({
        'username': username
    }, SECRET_KEY, algorithm = 'HS256')

    return token

def validate_token(token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return data['username']
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 403
    
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 403
        
        token = token.split(" ")[1] if token else ""
        try:
            username = validate_token(token)
        except Exception as e:
            return jsonify({'error': str(e)}), 403

        return f(username, *args, **kwargs)
    return decorated_function


@app.route('/messanger')
@token_required
def messanger(username):
    return render_template('messanger.html', username = username)


def db_connect():
    try:
        if app.config['DB_TYPE'] == 'postgres':
            conn = psycopg2.connect(
                host=app.config['DB_HOST'],
                database=app.config['DB_NAME'],
                user=app.config['DB_USER'],
                password=app.config['DB_PASSWORD'],
                port=app.config['DB_PORT']
            )
            cur = conn.cursor(cursor_factory=RealDictCursor)
        else:
            dir_path = path.dirname(path.realpath(__file__))
            db_path = path.join(dir_path, 'database.db')
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
        return conn, cur
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        return None, None


def db_close(conn, cur):
    if conn:
        conn.commit()
        cur.close()
        conn.close()

@app.route('/rgz/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    response = {
        'jsonrpc': '2.0',
        'id': data.get('id')
    }

    method = data.get('method')
    params = data.get('params', {})

    if method == 'register':
        login = params.get('login')
        password = params.get('password')

        if not login or not password:
            response['error'] = {
                'code': 5,
                'message': 'Введите логин/пароль'
            }
            return jsonify(response)

        conn, cur = db_connect()
        if not conn:
            response['error'] = {
                'code': -32000,
                'message': 'Database connection failed'
            }
            return jsonify(response)

        try:
            query = "SELECT * FROM users WHERE login = %s" if app.config['DB_TYPE'] == 'postgres' else \
                    "SELECT * FROM users WHERE login = ?"
            cur.execute(query, (login,))
            user = cur.fetchone()

            if user:
                response['error'] = {
                    'code': 6,
                    'message': 'Такой пользователь уже существует'
                }
            else:
                hashed_password = generate_password_hash(password)
                query = "INSERT INTO users (login, password) VALUES (%s, %s)" if app.config['DB_TYPE'] == 'postgres' else \
                        "INSERT INTO users (login, password) VALUES (?, ?)"
                cur.execute(query, (login, hashed_password))
                response['result'] = 'success'
        except Exception as e:
            response['error'] = {
                'code': -32001,
                'message': f'Database operation failed: {str(e)}'
            }
        finally:
            db_close(conn, cur)

    elif method == 'login':
        login = params.get('login')
        password = params.get('password')

        if not login or not password:
                response['error'] = {
                    'code': 5,
                    'message': 'Username and password are required'
                }
                return jsonify(response)
    
        conn, cur = db_connect()
        if not conn:
            response['error'] = {
                'code': -32000,
                'message': 'Database connection failed'
            }
            return jsonify(response)
        
        try:
            query = "SELECT * FROM users WHERE login = %s" if app.config["DB_TYPE"] == 'postgres' else \
                    "SELECT * FROM users WHERE login = ?"
            cur.execute(query, (login,))
            user = cur.fetchone()
            
            if not user: 
                response['error'] = {
                    'code': 7,
                    'message': 'Invalid login or password'
                }
            else: 
                stored_password = user['password']
                if check_password_hash(stored_password, password):
                    token = generate_token(user['login'])
                    response['result'] = {
                        'message': 'Авторизация успешна',
                        'token': token 
                    }
                else:
                    response['error'] = {
                        'code': 7,
                        'message': 'Invalid login or password'
                    }
        except Exception as e:
            response['error'] = {
                'code': -32001,
                'message': f'Database operation failed: {str(e)}'
            }
        finally:
            db_close(conn, cur)

    elif method == 'get_users':
        conn, cur = db_connect()
        if not conn:
            response['error'] = {
                'code': -32000,
                'message': 'Database connection failed'
            }
            return jsonify(response)

        try:
            query = "SELECT login FROM users" if app.config['DB_TYPE'] == 'postgres' else \
                    "SELECT login FROM users"
            cur.execute(query)
            users = cur.fetchall()

            response['result'] = {'users': [{'login': user['login']} for user in users]}
        except Exception as e:
            response['error'] = {
                'code': -32001,
                'message': f'Database operation failed: {str(e)}'
            }
        finally:
            db_close(conn, cur)

    elif method == 'get_messages':
        selected_user = params.get('user')
        username = params.get('username')

        if not selected_user or not username:
            response['error'] = {
                'code': 5,
                'message': 'Both username and selected user are required'
            }
            return jsonify(response)

        conn, cur = db_connect()
        if not conn:
            response['error'] = {
                'code': -32000,
                'message': 'Database connection failed'
            }
            return jsonify(response)

        try:
            query = "SELECT * FROM messages WHERE (sender = %s AND receiver = %s) OR (sender = %s AND receiver = %s)" if app.config['DB_TYPE'] == 'postgres' else \
                    "SELECT * FROM messages WHERE (sender = ? AND receiver = ?) OR (sender = ? AND receiver = ?)"
            cur.execute(query, (username, selected_user, selected_user, username))
            messages = cur.fetchall()

            response['result'] = {'messages': [{'text': msg['text']} for msg in messages]}
        except Exception as e:
            response['error'] = {
                'code': -32001,
                'message': f'Database operation failed: {str(e)}'
            }
        finally:
            db_close(conn, cur)

    elif method == 'send_message':
        selected_user = params.get('user')
        message_text = params.get('message')
        username = params.get('username')

        if not selected_user or not message_text or not username:
            response['error'] = {
                'code': 5,
                'message': 'Username, selected user and message are required'
            }
            return jsonify(response)

        conn, cur = db_connect()
        if not conn:
            response['error'] = {
                'code': -32000,
                'message': 'Database connection failed'
            }
            return jsonify(response)

        try:
            query = "INSERT INTO messages (sender, receiver, text) VALUES (%s, %s, %s)" if app.config['DB_TYPE'] == 'postgres' else \
                    "INSERT INTO messages (sender, receiver, text) VALUES (?, ?, ?)"
            cur.execute(query, (username, selected_user, message_text))

            response['result'] = 'Message sent successfully'
        except Exception as e:
            response['error'] = {
                'code': -32001,
                'message': f'Database operation failed: {str(e)}'
            }
        finally:
            db_close(conn, cur)

    else:
        response['error'] = {
            'code': -32601,
            'message': 'Method not found'
        }

    return jsonify(response)
