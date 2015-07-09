from flask import jsonify


class ValidationError(ValueError):
    pass


def not_modified():
    response = jsonify({'status': 304, 'error': 'not modified'})
    response.status_code = 304
    return response


def bad_request(message):
    response = jsonify({'status': 400, 'error': 'bad request',
                        'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({'status': 401, 'error': 'unauthorized',
                        'message': message})
    response.status_code = 401
    return response


def internal_error(message):
    response = jsonify({'status': 500, 'error': 'internal error',
                        'message': message})
    response.status_code = 500
    return response
