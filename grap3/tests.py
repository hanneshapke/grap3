#!flask/bin/python
import unittest

# from config import basedir
from grap3.app import db, app
from grap3.models import Grocery
from grap3.utils import is_grocery, get_or_create_grocery, get_grocery


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            'sqlite:////Users/hannes/Development/grap3/test.db'
        self.app = app.test_client()
        db.create_all()

        # create items
        self.item = Grocery(name='banana')
        db.session.add(self.item)
        self.item = Grocery(name='beer')
        db.session.add(self.item)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_is_grocery(self):
        self.assertTrue(is_grocery('beer'))
        self.assertFalse(is_grocery('chocolate'))

    def test_get_grocery(self):
        self.assertEqual(get_grocery('beer'), self.item)
        self.assertEqual(get_grocery('marmelade'), None)

    def test_set_grocery(self):
        self.assertEqual(get_or_create_grocery('beer'), self.item)
        # self.assertTrue(set_grocery('chocolade'))


if __name__ == '__main__':
    unittest.main()
