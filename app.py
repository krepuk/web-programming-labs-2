from flask import Flask
app = Flask(__name__)

@app.route("/")
@app.route("/web")
def start():
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