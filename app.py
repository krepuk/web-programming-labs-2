from flask import Flask, url_for, redirect, render_template, abort
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3

app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)


@app.route('/')
@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
            <head>
                <title>НГТУ, ФБ, Лабораторные работы</title>
            </head>
            <body>
                <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
            <ul>
                <li><a href="/lab1">Первая лабораторная</a></li>
            </ul>
            <ul>
                <li><a href="/lab2">Вторая лабораторная</a></li>
            </ul>
                        <ul>
                <li><a href="/lab3">Третья лабораторная</a></li>
            </ul>
                <h1>Web-сервер на flask</h1>
            <a href="/lab1/autor">autor</a>
            </body>
            <footer>
                ФИО: Репьюк Екатерина Дмитриевна, Группа: ФБИ-22, Курс: 3, Год: 2024
            </footer>
        </html>""", 200, {"X-Server": "sample"
                          }


@app.errorhandler(404)
def not_found(err):
    path = url_for("static", filename="404.jpg")
    css_path = url_for("static", filename="404.css")
    return f'''
<!doctype html>
<html>
    <head>
        <title>404 Страница не найдена</title>
        <link rel="stylesheet" type="text/css" href="{ css_path }">
    </head>
    <body>
        <div class="error-container">
            <h1>404 Страница не найдена</h1>
            <p>Извините, кажется эта страница не найдена</p>
            <p>Возможно, страница еще не создана или ее украли;)</p>
            <img src="{path}">
        </div>
    </body>
</html>
''', 404


@app.route('/lab1/error/400')
def error_400():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Ошибка 400</h1>
        <p>Допущена опечатка в ссылке</p>
    </body>
</html>
''', 400


@app.route('/lab1/error/401')
def error_401():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Ошибка 401</h1>
        <p>Проблема с аутентификацией или авторизацией на сайте</p>
    </body>
</html>
''', 401


@app.route('/lab1/error/402')
def error_402():
    return '''
<!doctype html>
<html>
    <head>
        <title>402 Payment Required</title>
    </head>
    <body>
        <h1>Ошибка 402</h1>
        <p>Нестандартная ошибка клиента, зарезервированная для использования в будущем</p>
    </body>
</html>
''', 402


@app.route('/lab1/error/403')
def error_403():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Ошибка 403</h1>
        <p>Доступ к запрашиваемой странице запрещен или у пользователя нет прав на просмотр контента</p>
    </body>
</html>
''', 403


@app.route('/lab1/error/405')
def error_405():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Ошибка 405</h1>
        <p>Mетод HTTP не разрешен веб-сервером для запрошенного URL-адреса</p>
    </body>
</html>
''', 405


@app.route('/lab1/error/418')
def error_418():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Ошибка 418</h1>
        <p>Cервер не может приготовить кофе, потому что он чайник</p>
    </body>
</html>
''', 418


@app.errorhandler(500)
def server_error(e):
    css_path = url_for("static", filename="404.css")
    return f'''
<!doctype html>
<html>
    <head>
        <title>Ошибка 500</title>
        <link rel="stylesheet" type="text/css" href="{ css_path }">
    </head>
    <body>
        <div class="error-container">
            <h1>Ошибка 500</h1>
            <p>P.S. кажется, ошибка в коде </p>
        </div>
    </body>
</html>
''', 500
