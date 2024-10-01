from flask import Flask, url_for, redirect, render_template
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
        </html>""", 200, {"X-Server": "sample"
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

@app.route('/lab1')
def lab1():
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
        <link rel="stylesheet" type="text/css" href="{ css_path }">
    </head>
    <body>
        <h1>Лабораторная 1</h1>
        <p>
            Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
        </p>
        <h2>Список роутов</h2>
        <ul>
            <li><a href="/index">Индекс</a></li>
            <li><a href="/lab1/autor">Данные об авторе</a></li>
            <li><a href="/lab1/oak">Дуб</a></li>
            <li><a href="/lab1/counter">Счетчик</a></li>
            <li><a href="/lab1/clear">Очищение</a></li>
            <li><a href="/lab1/info">Инфо</a></li>
            <li><a href="/lab1/created">Что-то создано</a></li>
            <li><a href="/lab1/error/400">Ошибка 400</a></li>
            <li><a href="/lab1/error/401">Ошибка 401</a></li>
            <li><a href="/lab1/error/402">Ошибка 402</a></li>
            <li><a href="/lab1/error/403">Ошибка 403</a></li>
            <li><a href="/lab1/error/405">Ошибка 405</a></li>
            <li><a href="/lab1/error/418">Ошибка 418</a></li>
            <li><a href="/lab1/trigger_error">Деление на ноль</a></li>
            <li><a href="/lab1/my_route">Мой роут</a></li>
        </ul>
        <a href="/">Вернуться на главную</a>
    </body>
</html>
'''

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

@app.route('/lab1/trigger_error')
def null_error():
    result = 1 / 0
    return str(result)

@app.errorhandler(500)
def server_error(e):
    css_path = url_for("static", filename="404.css")
    return f'''
<!doctype html>
<html>
    <head>
        <title>Ошибка 500</title>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <div class="error-container">
            <h1>Ошибка 500</h1>
            <p>P.S. На ноль делить нельзя</p>
        </div>
    </body>
</html>
''', 500

@app.route('/lab1/my_route')
def my_route():
    css_path = url_for("static", filename="404.css")
    path = url_for("static", filename="cat.jpg")
    return '''
<!doctype html>
<html>
    <head>
        <title>Новый роут</title>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <header>*Что-то на программистком*</header>
        <div class="content-container">
            <h1>Языки программирования</h1>
            <p>Python (МФА: [ˈpʌɪθ(ə)n]; в русском языке встречаются названия пито́н или па́йтон) — мультипарадигмальный высокоуровневый язык программирования общего назначения с динамической строгой типизацией и автоматическим управлением памятью, ориентированный на повышение производительности разработчика, читаемости кода и его качества, а также на обеспечение переносимости написанных на нём программ. Язык является полностью объектно-ориентированным в том плане, что всё является объектами.</p>
            <p>JavaScript это язык, который позволяет вам применять сложные вещи на web странице — каждый раз, когда на web странице происходит что-то большее, чем просто её статичное отображение — отображение периодически обновляемого контента, или интерактивных карт, или анимация 2D/3D графики, или прокрутка видео в проигрывателе, и т.д. — можете быть уверены, что скорее всего, не обошлось без JavaScript.</p>
            <p>C++ — это язык программирования, который был разработан в 80-х годах прошлого века как расширение языка C. Этот язык отличается от Си тем, что имеет больший набор возможностей, включая объектно-ориентированное программирование и шаблоны.</p>
            <img src="{path}">
        </div>
    </body>
</html>
'''.format(css_path=css_path, path=path), 200, {
        'Content-Language': 'ru', 'en'
        'Content-Length': '1348'
    }

@app.route('/lab2/a')
def a():
    return 'ok'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return "цветок: " + flower_list[flower_id]
    else:
        return "цветок: " + flower_list[flower_id]

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка: {name} </p>
    <p>Всего цветов: {len(flower_list)}</p>
    <p>Полный список: {flower_list}</p>
    </body>
</html>
'''
@app.route('/lab2/example')
def example():
    number = 2
    name = "Катя Репьюк"
    group = "ФБИ-22"
    curs = 3
    return render_template('example.html', number=number, name=name, group=group, curs=curs)
