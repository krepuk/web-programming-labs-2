from flask import Blueprint, render_template, request, redirect, abort
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import useri, articli
from flask_login import login_user, current_user, login_required, logout_user

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


@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form:
        return render_template('lab8/login.html', error='Введите логин!')
    if not password_form:
        return render_template('lab8/login.html', error='Введите пароль!')

    user = useri.query.filter_by(login=login_form).first()

    remember = False
    if request.form.get('remember'):
        remember = True

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember=remember)
            return redirect('/lab8/')

    return render_template('/lab8/login.html', error='Неверный логин/пароль!')


@lab8.route('/lab8/articles/', methods=['GET', 'POST'])
@login_required
def article_list():
    if current_user.is_authenticated:
        search_query = request.form.get('query', '').strip() if request.method == 'POST' else ''
        my_articles = articli.query.filter_by(login_id=current_user.id).all()
        public_articles = articli.query.filter(
            (articli.is_public == True) & (articli.login_id != current_user.id)
        ).all()

        results = None
        if search_query:
            results = articli.query.filter(
                (articli.title.ilike(f'%{search_query}%') | articli.article_text.ilike(f'%{search_query}%')) &
                ((articli.is_public == True) | (articli.login_id == current_user.id))
            ).all()

        return render_template(
            'lab8/articles.html',
            my_articles=my_articles,
            public_articles=public_articles,
            search_query=search_query,
            results=results
        )
    else:
        search_query = request.form.get('query', '').strip() if request.method == 'POST' else ''
        results = None
        if search_query:
            results = articli.query.filter(
                (articli.title.ilike(f'%{search_query}%') | articli.article_text.ilike(f'%{search_query}%')) &
                ((articli.is_public == True))
            ).all()
        public_articles = articli.query.filter(
            (articli.is_public == True)
        ).all()
        return render_template(
            'lab8/articles.html',
            public_articles=public_articles,
            search_query=search_query,
            results=results
        )


@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/') 


@lab8.route('/lab8/create/', methods = ['GET', 'POST'])
@login_required
def create():
        login_id = current_user.id
        if request.method == 'GET':
            return render_template('/lab8/create.html')
        
        title = request.form.get('title')
        article_text = request.form.get('article_text')
        is_public = request.form.get('is_public') == '1'

        if not (title and article_text):
            return render_template('/lab8/create.html', error='Введите текст и название статьи!')

        new_article = articli(login_id = login_id, title = title, article_text = article_text, is_public = is_public)
        db.session.add(new_article)
        db.session.commit()

        return redirect('/lab8/')

@lab8.route('/lab8/articles/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articli.query.filter_by(id=article_id, login_id=current_user.id).first()
    if not article:
        abort(404)

    db.session.delete(article)
    db.session.commit()
    return redirect('/lab8/articles/')