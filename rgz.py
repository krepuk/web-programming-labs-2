from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import jwt
from os import path

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
def login():
    return render_template('rgz/logins.html')


@app.route('/api', methods=['POST'])
def api_alias():
    return api() 


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


def generate_token(user_id):
    token = jwt.encode({
        'user_id': user_id
    }, SECRET_KEY, algorithm = 'HS256')

    return token


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
            query = "SELECT * FROM users WHERE login = %s" if app.config['DB_TYPE'] == 'postgres' else \
                    "SELECT * FROM users WHERE login = ?"
            cur.execute(query, (login,))
            user = cur.fetchone()

            if user:
                response['error'] = {
                    'code': 6,
                    'message': 'Username already exists'
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
                    token = generate_token(user['id'])
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

    else:
        response['error'] = {
            'code': -32601,
            'message': 'Method not found'
        }

    return jsonify(response)

def validate_token(token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return data['user_id']
    except jwt.ExpiredSignatureError:
        raise Exception('Token has expired')
    except jwt.InvalidTokenError:
        raise Exception('Invalid token')
    
@app.route('/rgz/json-rpc-api/protected', methods=['POST'])
def protected_api():
    data = request.json
    response = {
        'jsonrpc': '2.0',
        'id': data.get('id')
    }

    method = data.get('method')
    params = data.get('params', {})

    if method == 'get_protected_data':
        token = params.get('token')

        if not token:
            response['error'] = {
                'code': 5,
                'message': 'Token is required'
            }
            return jsonify(response)
        
        try:
            user_id = validate_token(token)
            
            conn, cur = db_connect()
            if not conn:
                response['error'] = {
                    'code': -32000,
                    'message': 'Database connection failed'
                }
                return jsonify(response)
            
            try:
                query = "SELECT * FROM protected_data WHERE user_id = %s" if app.config['DB_TYPE'] == 'postgres' else \
                        "SELECT * FROM protected_data WHERE user_id = ?"
                cur.execute(query, (user_id,))
                protected_data = cur.fetchone()
                
                if protected_data:
                    response['result'] = protected_data
                else:
                    response['error'] = {
                        'code': 8,
                        'message': 'No protected data found for this user'
                    }

            except Exception as e:
                response['error'] = {
                    'code': -32001,
                    'message': f'Database operation failed: {str(e)}'
                }
            finally:
                db_close(conn, cur)

        except Exception as e:
            response['error'] = {
                'code': 6,
                'message': f'Authentication failed: {str(e)}'
            }

    else:
        response['error'] = {
            'code': -32601,
            'message': 'Method not found'
        }

    return jsonify(response)