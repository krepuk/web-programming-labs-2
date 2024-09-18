from flask import Flask, url_for, redirect
app = Flask(__name__)

@app.route("/")
@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
            <body>
                <h1>Web-сервер на flask</h1>
            <a href="/lab1/autor">autor</a>
            </body>
        </html>""", 200, {"X-Server": "sample",
                          'Content-Type': 'text/plan; charset=utf-8'
                          }

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