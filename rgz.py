from flask import Blueprint, render_template, request, session, redirect, url_for
import json

rgz = Blueprint('rgz', __name__)

users = {}

@rgz.route('/rgz')
def rgzz():
    return render_template('rgz/rgz.html')

@rgz.route('/registers', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        
        # Вызов метода регистрации через JSON-RPC
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
