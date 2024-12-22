from flask import Blueprint, render_template, request, url_for, session, redirect


lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9')
def main():
        return render_template('lab9/index.html')


@lab9.route('/age', methods=['POST'])
def age():
    name = request.form['name']
    return render_template('lab9/age.html', name=name)

@lab9.route('/gender', methods=['POST'])
def gender():    
    name = request.form['name']
    age = request.form['age']
    return render_template('lab9/gender.html', name=name, age=age)

@lab9.route('/preference', methods=['POST'])
def preference():
    if 'name' not in request.form or 'age' not in request.form or 'gender' not in request.form:
        return "Ошибка: не все данные были переданы", 400

    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']

    return render_template('lab9/preference.html', name=name, age=age, gender=gender)


@lab9.route('/final', methods=['POST'])
def final():
    if 'name' not in request.form or 'age' not in request.form or 'gender' not in request.form or 'preference' not in request.form:
        return "Ошибка: не все данные были переданы", 400

    name = request.form['name']
    age = int(request.form['age'])
    gender = request.form['gender']
    preference = request.form['preference']

    if age >= 18:
        if gender == 'male':
            greeting = f"Дорогой {name}, поздравляю тебя с Новым годом! Желаю тебе успехов в работе, крепкого здоровья и счастья в личной жизни!"
        else:
            greeting = f"Дорогая {name}, поздравляю тебя с Новым годом! Желаю тебе успехов в карьере, крепкого здоровья и счастья в личной жизни!"
    else:
        if gender == 'male':
            greeting = f"Поздравляю тебя, {name}! Желаю тебе в новом году, новых друзей, приключений и побольше игрушек!!!"
        else:
            greeting = f"Поздравляю тебя, {name}! Желаю тебе в новом году, побольше приключений, игрушек и веселья!!!"

    if preference == 'cats':
        image = url_for('static', filename='giftcat.jpg')
        gift = "Вам принес подарок новогодний кот - 2025 год будет успешным!!! "
    else:
        image = url_for('static', filename='giftdog.jpg')
        gift = "Вам подарок принес новогодний щенок - 2025 год будет веселым!!!"

    greeting += f"<p>{gift}</p>"

    session['last_greeting'] = greeting
    session['last_image'] = image

    return render_template('lab9/final.html', message=greeting, image=image)

@lab9.route('/reset', methods=['POST'])
def reset():
    session.pop('last_greeting', None)
    session.pop('last_image', None)
    return redirect(url_for('lab9.main'))


@lab9.route('/lab9')
def main():
    if 'last_greeting' in session and 'last_image' in session:
        greeting = session['last_greeting']
        image = session['last_image']
        return render_template('lab9/final.html', message=greeting, image=image)

    return render_template('lab9/index.html')