from flask import Flask, request, jsonify, render_template, redirect, session
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

app = Flask(__name__)

app.secret_key = '040520240600'

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


@app.route('/rgz/registers')
def registers():
    return render_template('/rgz/registers.html')


@app.route('/rgz/logins')
def logins():
    return render_template('/rgz/logins.html')


@app.route('/api', methods=['POST'])
def api_alias():
    return api() 


@app.route('/rgz/messanger')
def messanger():
    if 'username' in session:
        return render_template('/rgz/messanger.html', username=session['username'])
    else:
        return redirect('/rgz/logins')  


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect('/rgz/logins')


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
                'message': 'Введите логин и пароль'
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
                    'message': 'Неверный логин или пароль'
                }
            else:
                stored_password = user['password']
                if check_password_hash(stored_password, password):
                    session['username'] = user['login']
                    response['result'] = {
                        'message': 'Авторизация успешна'
                    }
                else:
                    response['error'] = {
                        'code': 7,
                        'message': 'Неверный логин или пароль'
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
            query = "SELECT login FROM users"
            cur.execute(query)
            users = cur.fetchall()

            response['result'] = {
                'users': [{'login': user['login']} for user in users]
            }
        except Exception as e:
            response['error'] = {
                'code': -32001,
                'message': f'Database operation failed: {str(e)}'
            }
        finally:
            db_close(conn, cur)

    return jsonify(response)


@app.route('/json-rpc-api/messages', methods=['POST'])
def api_message():
    data = request.json
    response = {
        'jsonrpc': '2.0',
        'id': data.get('id')
    }
    
    method = data.get('method')
    params = data.get('params', {})

    if method == 'send_message':
        sender = params.get('sender')
        receiver = params.get('receiver')
        message = params.get('message')

        if not sender or not receiver or not message:
            response['error'] = {
                'code': 5,
                'message': 'Необходимо указать отправителя, получателя и текст сообщения'
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
            cur.execute(query, (sender, receiver, message))
            response['result'] = {
                'message': 'success'}
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")
            response['error'] = {
                'code': -32001,
                'message': f'Database operation failed: {str(e)}'
            }
        finally:
            db_close(conn, cur)

        return jsonify(response)

    elif method == 'get_messages':
        sender = params.get('sender')
        receiver = params.get('receiver')

        if not sender or not receiver:
            response['error'] = {
                'code': 5,
                'message': 'Необходимо указать отправителя и получателя'
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
            query = """
                SELECT * FROM messages 
                WHERE (sender = %s AND receiver = %s) 
                OR (sender = %s AND receiver = %s)
                ORDER BY timestamp ASC
            """ if app.config['DB_TYPE'] == 'postgres' else """
                SELECT * FROM messages 
                WHERE (sender = ? AND receiver = ?) 
                OR (sender = ? AND receiver = ?)
                ORDER BY timestamp ASC
            """
            cur.execute(query, (sender, receiver, receiver, sender))
            messages = cur.fetchall()

            response['result'] = {
                'messages': [{'sender': msg['sender'], 'receiver': msg['receiver'], 'text': msg['text'], 'timestamp': msg['timestamp']} for msg in messages]
            }
        except Exception as e:
            response['error'] = {
                'code': -32001,
                'message': f'Database operation failed: {str(e)}'
            }
        finally:
            db_close(conn, cur)

        return jsonify(response)

    elif method == 'get_message_id':
        sender = params.get('sender')
        receiver = params.get('receiver')
        text = params.get('text')

        print(f"Получены параметры: sender={sender}, receiver={receiver}, text={text}")

        if not sender or not receiver or not text:
            response['error'] = {
                'code': 5,
                'message': 'Необходимо указать отправителя, получателя и текст сообщения'
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
            query = "SELECT id FROM messages WHERE sender = %s AND receiver = %s AND text = %s"
            cur.execute(query, (sender, receiver, text))
            result = cur.fetchone()

            if result:
                message_id = result['id']
                response['result'] = {
                    'message_id': message_id
                }
            else:
                response['error'] = {
                    'code': -32002,
                    'message': 'Сообщение не найдено'
                }
        except Exception as e:
            response['error'] = {
                'code': -32001,
                'message': f'Database operation failed: {str(e)}'
            }
        finally:
            db_close(conn, cur)

        return jsonify(response)

    elif method == 'delete_message':
        message_id = params.get('message_id')
        if not message_id:
            response['error'] = {
                'code': 5,
                'message': 'Необходимо указать идентификатор сообщения'
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
            query = "DELETE FROM messages WHERE id = %s" if app.config['DB_TYPE'] == 'postgres' else \
                    "DELETE FROM messages WHERE id = ?"
            cur.execute(query, (message_id,))
            conn.commit()
            response['result'] = 'success'
            print(f"Сообщение с id {message_id} успешно удалено")

        except Exception as e:
            response['error'] = {
                'code': -32001,
                'message': f'Database operation failed: {str(e)}'
            }
        finally:
            db_close(conn, cur)

    return jsonify(response)