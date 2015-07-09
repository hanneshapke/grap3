from flask import (request, render_template, jsonify)
from .app import app
from .models import Grocery
from .utils import get_highest_match_from_groceries_from_redis
from .decorators import timer
from .errors import bad_request, internal_error


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/groceries/', methods=['GET'])
@timer
def get_all_groceries():
    return jsonify({'groceries': [i.name for i in Grocery.query.all()]})


@app.route('/api/groceries/<starts_with>', methods=['GET'])
@timer
def get_grocery(starts_with):
    return jsonify({
        'groceries': [i.name for i in Grocery.query.filter(
            Grocery.name.contains(starts_with))]})


@app.route('/api/recommendation/', methods=['GET'])
@timer
def get_most_common():
    if request.args.get('g') is '':
        return bad_request('Please add a request string')
    results = get_highest_match_from_groceries_from_redis(
        request.args.get('g'))
    if results[0] == 200:
        result_list = [{
            'name': i[0].decode('utf-8'),
            'common': '{0:.2f}'.format(i[1])} for i in results[1]]
        return jsonify(
            status=200,
            recommendations=result_list)
    return internal_error('Hm, something went wrong ...')
    # return jsonify(
    #     message=500,
    #     recommendation=[])
