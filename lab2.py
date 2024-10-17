from flask import Blueprint, url_for, redirect
lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/a')
def a():
    return 'ok'


@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']


@lab2.route('/lab2/flowers/<int:flower_id>')
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


@lab2.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.lab2end(name)
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


@lab2.route('/lab2/add_flower/')
def flower_f():
    return 'Вы не задали имя цветка', 400


@lab2.route('/lab2/all_flowers')
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


@lab2.route('/lab2/clear_flowers')
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


@lab2.route('/lab2/example')
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


@lab2.route('/lab2/')
def laba2():
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


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)


@lab2.route('/lab2/calc/')
def calc_redirect():
    return redirect('/lab2/calc/1/1')


@lab2.route('/lab2/calc/<int:a>')
def calc_redirect_a(a):
    return redirect(f'/lab2/calc/{a}/1')


@lab2.route('/lab2/calc/<int:a>/<int:b>')
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


@lab2.route('/lab2/books')
def books_list():
    return render_template('books.html', books=books)

cats = [
    {"name": "Британская кошка", "description": "Отличается вредным характером", "image": "cat1.jpg"},
    {"name": "Мейн-кун", "description": "Отличается огромными габаритами", "image": "cat2.jpg"},
    {"name": "Сфинкс", "description": "Отличается отсутствием шерсти", "image": "cat3.jpg"},
    {"name": "Сиамская кошка", "description": "Имеет отличительную окраску и вредный характер", "image": "cat4.jpg"},
    {"name": "Персидская кошка", "description": "Имеет плоскую морду", "image": "cat5.jpg"}
]


@lab2.route('/lab2/cats')
def cats_list():
   return render_template('cats.html', cats=cats)

