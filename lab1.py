from flask import Blueprint, url_for, redirect
lab1 = Blueprint('lab1', __name__)


@lab1.route('/index')
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
        <ul>
            <li><a href="/lab2">Вторая лабораторная</a></li>
        </ul>
        <footer>
             ФИО: Репьюк Екатерина Дмитриевна, Группа: ФБИ-22, Курс: 3, Год: 2024
        </footer>
    </body>
</html>
'''


@lab1.route("/lab1/autor")
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


@lab1.route("/lab1/oak")
def oak():
    path = url_for("static", filename="lab1/oak.jpg")
    css_path = url_for("static", filename="lab1/lab1.css")
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


@lab1.route('/lab1/counter')
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


@lab1.route('/lab1/clear')
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


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/autor")


@lab1.route('/lab1/created')
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


@lab1.route('/lab1')
def lab():
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


@lab1.route('/lab1/trigger_error')
def null_error():
        return 1/0


@lab1.route('/lab1/my_route')
def my_route():
    css_path = url_for("static", filename="lab1/404.css")
    path = url_for("static", filename="lab1/cat.jpg")
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