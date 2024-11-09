from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form', methods=['GET'])
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    elif x2 == '0':
        return render_template('lab4/div.html', error='На ноль делить нельзя!')
    
    x1 = int(x1)
    x2 = int(x2)
    result = x1 / x2
    
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sum-form', methods=['GET'])
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1', '0')
    x2 = request.form.get('x2', '0')
    
    x1 = int(x1) if x1.isdigit() else 0
    x2 = int(x2) if x2.isdigit() else 0

    result = x1 + x2
    
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/mul-form', methods=['GET'])
def mul_form():
    return render_template('lab4/mul-form.html')

@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1', '1')
    x2 = request.form.get('x2', '1')

    x1 = int(x1) if x1.isdigit() else 1
    x2 = int(x2) if x2.isdigit() else 1

    result = x1 * x2
    
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sub-form', methods=['GET'])
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/pow-form', methods=['GET'])
def pow_form():
    return render_template('lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])
def pow():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')
    elif x1 == '0' and x2 == '0':
        return render_template('lab4/pow.html', error='Оба поля не могут быть нулями!')
    
    x1 = int(x1)
    x2 = int(x2)
    result = x1 ** x2
    
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)


tree_count = 0

@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count )
    
    operation = request.form.get('operation')

    if operation == 'cut':
        if tree_count > 0:
            tree_count -= 1
    elif operation == 'plant':
        tree_count += 1
    
    return redirect('/lab4/tree')

users = [
    {'login': 'alex', 'password': '123', 'name': 'Alex Smith', 'gender': 'male'},
    {'login': 'bob', 'password': '666', 'name': 'Bob Johnson', 'gender': 'male'},
    {'login': 'jessi', 'password': '777', 'name': 'Jessi Brown', 'gender': 'female'},
    {'login': 'kim', 'password': '555', 'name': 'Kim Lee', 'gender': 'female'},
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            name = next(user['name'] for user in users if user['login'] == login)
        else:
            authorized = False
            login = ''
            name = ''
        return render_template("/lab4/login.html", authorized=authorized, login=login, name=name)
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login:
        error = 'Не введён логин'
        return render_template('/lab4/login.html', error=error, authorized=False, login=login)
    
    if not password:
        error = 'Не введён пароль'
        return render_template('/lab4/login.html', error=error, authorized=False, login=login)

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            return redirect('/lab4/login')
    
    error = 'Неверные логин и/или пароль'
    return render_template('/lab4/login.html', error=error, authorized=False, login=login)


@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'POST':
        temperature = request.form.get('temperature')
        
        if not temperature:
            message = 'Ошибка: не задана температура'
            snowflakes = ''
        else:
            temperature = float(temperature)
            snowflakes = ''  
            if temperature < -12:
                message = 'Не удалось установить температуру — слишком низкое значение'
            elif temperature > -1:
                message = 'Не удалось установить температуру — слишком высокое значение'
            elif -12 <= temperature <= -9:
                message = f'Установлена температура: {temperature}°С'
                snowflakes = '❄️❄️❄️'
            elif -8 <= temperature <= -5:
                message = f'Установлена температура: {temperature}°С'
                snowflakes = '❄️❄️'
            elif -4 <= temperature <= -1:
                message = f'Установлена температура: {temperature}°С'
                snowflakes = '❄️'
            else:
                message = f'Установлена температура: {temperature}°С'
        
        return render_template('/lab4/fridge.html', message=message, snowflakes=snowflakes)
    
    return render_template('/lab4/fridge.html')


@lab4.route('/lab4/grain_order', methods=['GET', 'POST'])
def grain_order():
    if request.method == 'POST':
        grain_type = request.form.get('grain_type')
        weight = request.form.get('weight')
        
        if not weight:
            error = 'Ошибка: не указан вес'
            return render_template('/lab4/grain_order.html', error=error)
        
        weight = float(weight)
        
        if weight <= 0:
            error = 'Ошибка: вес должен быть больше 0'
            return render_template('/lab4/grain_order.html', error=error)
        
        if weight > 500:
            error = 'Ошибка: такого объёма сейчас нет в наличии'
            return render_template('/lab4/grain_order.html', error=error)
        
        prices = {
            'ячмень': 12345,
            'овёс': 8522,
            'пшеница': 8722,
            'рожь': 14111
        }
        
        price_per_ton = prices.get(grain_type)
        
        if not price_per_ton:
            error = 'Ошибка: неверный тип зерна'
            return render_template('/lab4/grain_order.html', error=error)
        
        total_cost = price_per_ton * weight
        
        if weight > 50:
            discount = total_cost * 0.1
            total_cost -= discount
            discount_message = f'Применена скидка за большой объём: {discount} руб'
        else:
            discount_message = ''
        
        message = f'Заказ успешно сформирован. Вы заказали {grain_type}. Вес: {weight} т. Сумма к оплате: {total_cost} руб'
        return render_template('/lab4/grain_order.html', message=message, discount_message=discount_message)
    
    return render_template('/lab4/grain_order.html')


@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        name = request.form.get('name')
        gender = request.form.get('gender')
        
        if not login or not password or not name or not gender:
            error = 'Ошибка: все поля должны быть заполнены'
            return render_template('/lab4/register.html', error=error)
        
        for user in users:
            if user['login'] == login:
                error = 'Ошибка: логин уже занят'
                return render_template('/lab4/register.html', error=error)
        
        users.append({'login': login, 'password': password, 'name': name, 'gender': gender})
        return redirect('/lab4/users')  # Перенаправление на страницу со списком пользователей
    
    return render_template('/lab4/register.html')

@lab4.route('/lab4/users', methods=['GET', 'POST'])
def users_list():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'delete':
            login = session['login']
            users[:] = [user for user in users if user['login'] != login]
            session.pop('login', None)
            return redirect('/lab4/login')
        elif action == 'edit':
            login = session['login']
            user = next(user for user in users if user['login'] == login)
            user['password'] = request.form.get('password')
            user['name'] = request.form.get('name')
            user['gender'] = request.form.get('gender')
            return redirect('/lab4/users')
    
    return render_template('/lab4/users.html', users=users)


