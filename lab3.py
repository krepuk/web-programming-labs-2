from flask import Blueprint, url_for, redirect, render_template, request, make_response
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    age = request.cookies.get('age')
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')

    if drink =='coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
        price = request.args.get('price', type=int)
        return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        color = request.form.get('color')
        backgroundcolor = request.form.get('backgroundcolor')
        fontsize = request.form.get('fontsize')
        linkcolor = request.form.get('linkcolor')
        if color and backgroundcolor:
            resp = make_response(redirect('/lab3/settings'))
            resp.set_cookie('color', color)
            resp.set_cookie('backgroundcolor', backgroundcolor)
            resp.set_cookie('fontsize', fontsize)
            resp.set_cookie('linkcolor', linkcolor)
            return resp

    color = request.cookies.get('color')
    backgroundcolor = request.cookies.get('backgroundcolor')
    fontsize = request.cookies.get('fontsize')
    linkcolor = request.cookies.get('linkcolor')
    resp = make_response(render_template('lab3/settings.html', color=color, backgroundcolor=backgroundcolor,fontsize=fontsize, linkcolor=linkcolor))
    return resp


@lab3.route('/lab3/formtrain')
def formTrain():
    ticketCost = 0
    fio = request.args.get('fio')
    place = request.args.get('place')
    linen = request.args.get('linen')
    luggage = request.args.get('luggage')
    age = request.args.get('age')
    start = request.args.get('start')
    end = request.args.get('end')
    date = request.args.get('date')
    insurance = request.args.get('insurance')

    argsNames = [fio, age, start, end, date]

    check = False

    errors = {
        'fio': '',
        'age': '',
        'start': '',
        'end': '',
        'date': ''
    }

    if fio == '':
        errors['fio'] = 'Заполните поле!'
    else:
        errors['fio'] = ''

    if age == '':
        errors['age'] = 'Заполните поле!'
    elif  type(age) == str and (int(age) < 0 or int(age) > 120):
        errors['age'] = 'Введите реальный возраст!'
    else:
        errors['age'] = ''

    if start == '':
        errors['start'] = 'Заполните поле!'
    else:
        errors['start'] = ''

    if end == '':
        errors['end'] = 'Заполните поле!'
    else:
        errors['end'] = ''

    if date == '':
        errors['date'] = 'Заполните поле!'
    else:
        errors['date'] = ''

    if all(argsNames) and (int(age) >= 0 and int(age) <= 120):
        check = True

    if check == True:
        if int(age) > 17:
            ticketCost += 1000
        else:
            ticketCost += 700

        if place == 'нижняя':
            ticketCost += 100
        elif place == 'нижняя боковая':
            ticketCost += 100
        
        if linen is not None:
            ticketCost += 75
        
        if luggage is not None:
            ticketCost += 250
        
        if insurance is not None:
            ticketCost += 150
        
    return render_template('lab3/formtrain.html', fio=fio, place=place, linen=linen, luggage=luggage,
                        age=age, start=start, end=end, date=date, insurance=insurance, errors=errors,
                        argsNames=argsNames, check=check, ticketCost=ticketCost)


@lab3.route('/lab3/clear_cookies')
def clear_cookies():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('backgroundcolor')
    resp.delete_cookie('fontsize')
    resp.delete_cookie('linkcolor')
    return resp


cats = [
    {"breed": "Британская короткошерстная", "price": 500, "color": "Серый", "origin": "Великобритания"},
    {"breed": "Сиамская", "price": 600, "color": "Коричневый", "origin": "Таиланд"},
    {"breed": "Мейн-кун", "price": 700, "color": "Рыжий", "origin": "США"},
    {"breed": "Русская голубая", "price": 550, "color": "Голубой", "origin": "Россия"},
    {"breed": "Бенгальская", "price": 800, "color": "Пятнистый", "origin": "США"},
    {"breed": "Сфинкс", "price": 900, "color": "Безволосый", "origin": "Канада"},
    {"breed": "Абиссинская", "price": 650, "color": "Охра", "origin": "Эфиопия"},
    {"breed": "Шотландская вислоухая", "price": 500, "color": "Голубой", "origin": "Великобритания"},
    {"breed": "Бурманская", "price": 750, "color": "Коричневый", "origin": "Бирма"},
    {"breed": "Норвежская лесная", "price": 600, "color": "Серебристый", "origin": "Норвегия"},
    {"breed": "Американский керл", "price": 550, "color": "Черный", "origin": "США"},
    {"breed": "Персидская", "price": 850, "color": "Белый", "origin": "Иран"},
    {"breed": "Экзотическая короткошерстная", "price": 700, "color": "Голубой", "origin": "США"},
    {"breed": "Девон-рекс", "price": 650, "color": "Рыжий", "origin": "Великобритания"},
    {"breed": "Корниш-рекс", "price": 500, "color": "Пятнистый", "origin": "Великобритания"},
    {"breed": "Манчкин", "price": 750, "color": "Голубой", "origin": "США"},
    {"breed": "Саванна", "price": 900, "color": "Пятнистый", "origin": "США"},
    {"breed": "Ориентальная", "price": 600, "color": "Голубой", "origin": "США"},
    {"breed": "Сибирская", "price": 550, "color": "Голубой", "origin": "Россия"},
    {"breed": "Тойгер", "price": 800, "color": "Пятнистый", "origin": "США"}
]


@lab3.route('/lab3/cats')
def cats():
    min_price = request.args.get('min')
    max_price = request.args.get('max')
    
    showList = []

    errors = {}


    if min_price == '':
        errors['min'] = 'Заполните поле!'
    else:
        errors['min'] = ''

    if max_price == '':
        errors['max'] = 'Заполните поле!'
    else:
        errors['max'] = ''

    if min_price and max_price:
        for cat in cats:
            if cat['price'] >= int(min_price) and cat['price'] <= int(max_price):
                showList.append(cat)

    return render_template('/lab3/cats.html', min=min_price, max=max_price, errors=errors, cats=cats, showList=showList)

