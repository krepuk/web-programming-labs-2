from flask import Flask, url_for
app = Flask(__name__)

@app.route("/")
@app.route("/web")
def web():
    return """<!doctype html>
        <html>
            <body>
                <h1>Web-сервер на flask</h1>
            <a href="/autor">autor</a>
            </body>
        </html>"""

@app.route("/autor")
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
                <a href="/web">web</a>
            </body>
        </html>"""

@app.route("/lab1/oak")
def oak():
    path = url_for("static", filename="oak.jpg")
    return '''
    <!doctype html>
        <html>
            <body>
                <h1>Дуб</h1>
                <img src="''' + path + '''">
            </body>
        </html>'''

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
    </body>
</html>
'''