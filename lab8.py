from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash
from db import db
from db.models import useri
from flask_login import login_user, current_user

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    if current_user.is_authenticated:
        user = current_user.login
    else:
        user = 'Анонимус' 
    return render_template('/lab8/lab8.html', user=user)

@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    
    if not login_form:
        return render_template('lab8/register.html', error='Пустой логин!')
    if not password_form:
        return render_template('lab8/register.html', error='Пустой пароль!')

    login_exists = useri.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует!')
    
    password_hash = generate_password_hash(password_form)
    
    new_user = useri(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user, remember=False)
    
    return redirect('/lab8/')