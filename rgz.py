from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash
import sqlite3
from os import path

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
    else:
        response['error'] = {
            'code': -32601,
            'message': 'Method not found'
        }

    return jsonify(response)


@app.route('/rgz/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    response = {
        'jsonrpc': '2.0',
        'id': data.get('id')
    }

