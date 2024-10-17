from flask import Flask, url_for, redirect, render_template, abort
from lab1 import lab1

app = Flask(__name__)
app.register_blueprint(lab1)


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


@app.route('/lab1/trigger_error')
def null_error():
        return 1/0


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
        css_path = url_for("static", filename="main.css")
        if 0 <= flower_id < len(flower_list):
            flower = flower_list[flower_id]
        return f'''
        <!doctype html>
        <html>
            <head>
                <title>Цветок</title>
                <link rel="stylesheet" href="{ url_for('static', filename='main.css') }">
            </head>
            <body>
                <h1>Цветок: {flower}</h1>
                <p><a href="/lab2/all_flowers">Показать все цветы</a></p>
            </body>
        </html>
        '''


@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <header>
        <a href="/">Главное меню</a>
    </header>
    <body>
        <h1>Добавлен новый цветок</h1>
        <p>Название нового цветка: {name} </p>
        <p>Всего цветов: {len(flower_list)}</p>
        <p>Полный список: {flower_list}</p>
    </body>
</html>
'''


@app.route('/lab2/add_flower/')
def flower_f():
    return 'Вы не задали имя цветка', 400


@app.route('/lab2/all_flowers')
def all_flowers():
    css_path = url_for("static", filename="main.css")
    return f'''
    <!doctype html>
    <html>
        <head>
            <link rel="stylesheet" href="{ url_for('static', filename='main.css') }">
        </head>
        <body>
            <h1>Цветы</h1>
            <p>Всего цветов: {len(flower_list)}</p>
            <p>Список цветов: {', '.join(flower_list)}</p>
            <p><a href="/lab2/clear_flowers">Очистить список цветов</a></p>
        </body>
    </html>
    '''


@app.route('/lab2/clear_flowers')
def clear_flowers():
    css_path = url_for("static", filename="main.css")
    global flower_list
    flower_list = []
    return f'''
    <!doctype html>
    <html>
        <head>
            <link rel="stylesheet" href="{ url_for('static', filename='main.css') }">
        </head>
        <body>
            <h1>Список цветов очищен</h1>
            <p>Всего цветов: {len(flower_list)}</p>
            <p><a href="/lab2/all_flowers">Показать все цветы</a></p>
        </body>
    </html>
    '''


@app.route('/lab2/example')
def example():
    number = 2
    name = "Катя Репьюк"
    group = "ФБИ-22"
    curs = 3
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 320}
        ]
    return render_template('example.html', number=number, name=name, group=group, curs=curs, fruits=fruits)


@app.route('/lab2/')
def lab2():
    return f'''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 2</title>
        <link rel="stylesheet" href="{ url_for('static', filename='main.css') }">
    </head>
    <body>
        <h1>Лабораторная 2</h1>
        <h2>Список роутов</h2>
        <ul>
            <li><a href="/lab2/a">А</a></li>
            <li><a href="/lab2/a/">/А</a></li>
            <li><a href="/lab2/flowers/<int:flower_id>">Цветок</a></li>
            <li><a href="/lab2/add_flower/<name>'">Добавить цветок</a></li>
            <li><a href="/lab2/all_flowers">Все цветы</a></li>
            <li><a href="/lab2/clear_flowers">Очистить список цветов</a></li>
            <li><a href="/lab2/example">Пример</a></li>
            <li><a href="/lab2/filters">Фильтры</a></li>
            <li><a href="/lab2/calc/">Калькулятор</a></li>
            <li><a href="/lab2/calc/<int:a>">Калькулятор А</a></li>
            <li><a href="/lab2/calc/<int:a>/<int:b>">Калькулятор А/B</a></li>
            <li><a href="/lab2/books">Книги</a></li>
            <li><a href="/lab2/cats">Котики</a></li>
        </ul>
        <a href="/">Вернуться на главную</a>
    </body>
</html>
'''


@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)


@app.route('/lab2/calc/')
def calc_redirect():
    return redirect('/lab2/calc/1/1')


@app.route('/lab2/calc/<int:a>')
def calc_redirect_a(a):
    return redirect(f'/lab2/calc/{a}/1')


@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    css_path = url_for("static", filename="main.css")
    sum_result = a + b
    diff_result = a - b
    prod_result = a * b
    div_result = a / b if b != 0 else "Деление на ноль"
    step_result = a ** b
    return f'''
    <!doctype html>
    <html>
        <head>
            <title>Репьюк Катя</title>
            <link rel="stylesheet" href="{ url_for('static', filename='main.css') }">
        </head>
        <header>
            WEB-программирование, часть 2. Лабораторная работа 2
        <a href="/">Главное меню</a>
        </header>
        <body>
            <h1>Результаты вычислений</h1>
            <p>Сумма: {a} + {b} = {sum_result}</p>
            <p>Разность: {a} - {b} = {diff_result}</p>
            <p>Произведение: {a} * {b} = {prod_result}</p>
            <p>Деление: {a} / {b} = {div_result}</p>
            <p>Возведение в степень: {a} ^ {b} = {step_result}</p>
        </body>
        <footer>
            &copy; Репьюк Катя, ФБИ-22, 3 курс, 2024
        </footer>
    </html>
    '''

books = [
    {"author": "Джордж Оруэлл", "title": "1984", "genre": "Научная фантастика", "pages": 328},
    {"author": "Рэй Брэдбери", "title": "451 градус по Фаренгейту", "genre": "Научная фантастика", "pages": 224},
    {"author": "Нора Сакавич", "title": "Лисья нора", "genre": "Молодежная литература", "pages": 336},
    {"author": "Джейн Остин", "title": "Гордость и предубеждение", "genre": "Роман", "pages": 432},
    {"author": "Михаил Булгаков", "title": "Мастер и Маргарита", "genre": "Фантастика", "pages": 480},
    {"author": "Эрих Мария Ремарк", "title": "Три товарища", "genre": "Роман", "pages": 480},
    {"author": "Роулинг Джоан Кэтлин", "title": "Гарри Поттер и философский камень", "genre": "Фэнтези", "pages": 352},
    {"author": "Лев Толстой", "title": "Война и мир", "genre": "Роман", "pages": 1225},
    {"author": "Роулинг Джоан Кэтлин", "title": "Гарри Поттер и Тайная комната", "genre": "фэнтези", "pages": 480},
    {"author": "Джером Д. Сэлинджер", "title": "Над пропастью во ржи", "genre": "Роман", "pages": 277}
]


@app.route('/lab2/books')
def books_list():
    return render_template('books.html', books=books)

cats = [
    {"name": "Британская кошка", "description": "Отличается вредным характером", "image": "cat1.jpg"},
    {"name": "Мейн-кун", "description": "Отличается огромными габаритами", "image": "cat2.jpg"},
    {"name": "Сфинкс", "description": "Отличается отсутствием шерсти", "image": "cat3.jpg"},
    {"name": "Сиамская кошка", "description": "Имеет отличительную окраску и вредный характер", "image": "cat4.jpg"},
    {"name": "Персидская кошка", "description": "Имеет плоскую морду", "image": "cat5.jpg"}
]


@app.route('/lab2/cats')
def cats_list():
   return render_template('cats.html', cats=cats)

