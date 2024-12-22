from flask import Blueprint, render_template, request, abort, make_response, jsonify

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9')
def main():
        return render_template('lab9/index.html')