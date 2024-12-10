from flask import Blueprint, render_template, request, abort, make_response, jsonify
import json

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7')
def main():
    return render_template('lab7/index.html')


films = [
    {
        "title": "Harry Potter and the Philosopher's Stone",
        "title_ru": "Гарри Поттер и философский камень",
        "year": 2001,
        "description": "Первый фильм из серии о мальчике-волшебнике Гарри Поттере. В 11 лет Гарри узнает, что он волшебник и его родители были знаменитыми магами. Он отправляется в школу магии и волшебства Хогвартс, где знакомится с Ронами Уизли и Гермионой Грейнджер. Вместе они сталкиваются с тайнами философского камня, который может даровать вечную жизнь. Гарри должен предотвратить его кражу злодеем Волан-де-Мортом."
    },
    {
        "title": "Harry Potter and the Chamber of Secrets",
        "title_ru": "Гарри Поттер и тайная комната",
        "year": 2002,
        "description": "Второй фильм из серии о мальчике-волшебнике Гарри Поттере. После летних каникул Гарри возвращается в Хогвартс, где его ждут новые приключения. В школе начинают происходить загадочные события, связанные с тайной комнатой, которую, по легенде, открыл один из основателей школы, Салазар Слизерин. Гарри, Рон и Гермиона должны раскрыть тайну, чтобы спасти школу от ужасных последствий."
    },
    {
        "title": "Harry Potter and the Prisoner of Azkaban",
        "title_ru": "Гарри Поттер и узник Азкабана",
        "year": 2004,
        "description": "Третий фильм из серии о мальчике-волшебнике Гарри Поттере. В Хогвартс прибывает опасный преступник Сириус Блэк, который якобы предает родителей Гарри. Гарри, Рон и Гермиона должны разгадать тайну прошлого и предотвратить новые преступления. В этом фильме также впервые появляются Дementors — мрачные существа, охраняющие тюрьму Азкабан."
    },
    {
        "title": "Harry Potter and the Goblet of Fire",
        "title_ru": "Гарри Поттер и Кубок огня",
        "year": 2005,
        "description": "Четвертый фильм из серии о мальчике-волшебнике Гарри Поттере. В Хогвартсе проходит Турнир Трех Волшебников, где участвуют три величайших школы магии. Гарри неожиданно становится участником турнира, хотя ему еще нет 17 лет. Вместе с друзьями он должен пройти три смертельно опасных испытания, чтобы выиграть Кубок огня. Однако, за кулисами скрывается зловещий план Волан-де-Морта, который стремится вернуться к власти."
    }
]


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    return films[id]


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def delete_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    del films[id]
    return '', 204


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = request.get_json()
    if film['description'] == '':
        return {'description': 'Заполните описание'}, 400
    films[id] = film
    return films[id]


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    films.append(film)
    new_index = len(films) - 1
    response = make_response(json.dumps(new_index))
    response.headers['Content-Type'] = 'application/json'
    return response, 201