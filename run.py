# from flask import Flask
# from flask.ext.sqlalchemy import SQLAlchemy
# import os


# app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])
# db = SQLAlchemy(app)

# from models import Grocery, GroceryList  # noqa


# @app.route('/')
# def hello():
#     return "Hello World!"


# @app.route('/<name>')
# def hello_name(name):
#     return "Hello {}!".format(name)

# if __name__ == '__main__':
#     app.run()


from grap3.app import app
app.run(debug=True)
