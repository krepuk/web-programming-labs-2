from flask import Flask, url_for, redirect
app = Flask(__name__)

@app.route("/")
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
                <h1>Web-сервер на flask</h1>
            <a href="/lab1/autor">autor</a>
            </body>
            <footer>
                ФИО: Репьюк Екатерина Дмитриевна, Группа: ФБИ-22, Курс: 3, Год: 2024
            </footer>
        </html>""", 200, {"X-Server": "sample",
                          'Content-Type': 'text/plan; charset=utf-8'
                          }

@app.route('/index')
def index():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        <ul>
            <li><a href="/lab1">Первая лабораторная</a></li>
        </ul>
        <footer>
             ФИО: Репьюк Екатерина Дмитриевна, Группа: ФБИ-22, Курс: 3, Год: 2024
        </footer>
    </body>
</html>
'''

@app.route("/lab1/autor")
def author():
    name = "Репьюк Екатерина Дмитриевна"
    group = "ФБИ-22"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Группа: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""

@app.route("/lab1/oak")
def oak():
    path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")
    return f'''
    <!doctype html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="{css_path}">
            </head>
            <body>
                <h1>Дуб</h1>
                <img src="{path}">
            </body>
        </html>'''

count = 0 
@app.route('/lab1/counter')
def counter():
    global count
    count += 1 
    return '''
<!doctype html>
<html>
    <body>
        <a href="/lab1/clear">Очищение</a>
        Cколько раз вы сюда заходили: ''' + str(count) + '''
    </body>
</html>
'''
@app.route('/lab1/clear')
def clear_counter():
    global count
    count = 0
    return '''
<!doctype html>
<html>
    <body>
        Счётчик очищен. <a href="/lab1/counter">Вернуться к счётчику</a>
    </body>
</html>
'''

@app.route("/lab1/info")
def info():
    return redirect("/lab1/autor")

@app.route('/lab1/created')
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
       <div><i>что-то создано....но что непонятно....</i></div>
    </body>
</html>
''', 201

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404

@app.route('/lab1')
def lab1():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <h1>Лабораторная 1</h1>
        <p>
            Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
        </p>
        <a href="/">Вернуться на главную</a>
    </body>
</html>
'''

@app.route('/error/400')
def error_400():
    return '''
<!doctype html>
<html>
    <head>
        <title>Код 400</title>
    </head>
    <body>
        <h1>400 Bad Request</h1>
        <p>Сервер не может или не будет обрабатывать запрос из-за очевидной ошибки клиента.</p>
    </body>
</html>
''', 400

@app.route('/error/401')
def error_401():
    return '''
<!doctype html>
<html>
    <head>
        <title>Код 401</title>
    </head>
    <body>
        <h1>401 Unauthorized</h1>
        <p>Запрос не был применен, так как отсутствуют действительные учетные данные для целевого ресурса.</p>
    </body>
</html>
''', 401

@app.route('/error/402')
def error_402():
    return '''
<!doctype html>
<html>
    <head>
        <title>Код 402</title>
    </head>
    <body>
        <h1>402 Payment Required</h1>
        <p>Этот код зарезервирован для будущего использования.</p>
    </body>
</html>
''', 402

@app.route('/error/403')
def error_403():
    return '''
<!doctype html>
<html>
    <head>
        <title>Код 403</title>
    </head>
    <body>
        <h1>403 Forbidden</h1>
        <p>У клиента нет прав доступа к содержимому, поэтому сервер отказывается дать надлежащий ответ.</p>
    </body>
</html>
''', 403

@app.route('/error/405')
def error_405():
    return '''
<!doctype html>
<html>
    <head>
        <title>Код 405</title>
    </head>
    <body>
        <h1>405 Method Not Allowed</h1>
        <p>Метод, указанный в запросе, не разрешен для указанного ресурса.</p>
    </body>
</html>
''', 405

@app.route('/error/418')
def error_418():
    return '''
<!doctype html>
<html>
    <head>
        <title>Код 418</title>
    </head>
    <body>
        <h1>418 I'm a teapot</h1>
        <p>Сервер отказывается варить кофе, потому что является чайником.</p>
    </body>
</html>
''', 418
