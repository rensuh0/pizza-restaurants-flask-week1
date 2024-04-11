import pytest
from app import app, db
from flask_testing import TestCase
import json

class AppTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index(self):
        response = self.client.get('/')
        self.assert200(response)
        self.assertEqual(response.json, {"index": "Welcome to the Pizza-Restaurant RESTful API"})

    def test_get_restaurants(self):
        response = self.client.get('/restaurants')
        self.assert200(response)


if __name__ == '__main__':
    pytest.main(["test_app.py", "-v"])
