from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
# from api.app import create_app
import os

from grap3.app import app, db
app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def createdb():
    # app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

# @manager.command
# def test():
#     from subprocess import call
#     call(['nosetests', '-v',
#           '--with-coverage', '--cover-package=api', '--cover-branches',
#           '--cover-erase', '--cover-html', '--cover-html-dir=cover'])


@manager.command
def test():
    import unittest
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///Users/hannes/tmp/test.db'
    # from config import TestingConfig
    # app.config.from_object(TestingConfig)
    tests = unittest.TestLoader().discover('grap3')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
