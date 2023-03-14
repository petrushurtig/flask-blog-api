import json
from flask_testing import TestCase
from flask_bcrypt import generate_password_hash

from app import app
from src.db.config.db import db
from src.db.models.post import Post
from src.db.models.user import User

class TestPostRoutes(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_posts_is_empty(self):
        response = self.client.get('/v1/posts/')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        items = response_data['items']
        self.assertEqual(len(items), 0)

    def test_create_post(self):
        password_hash = generate_password_hash("password").decode("utf-8")
        user = User(name='testuser', email='testuser@test.com', password=password_hash)
        db.session.add(user)
        db.session.commit()

        post = Post(title="title", content="content", user_id=1,)
        db.session.add(post)
        db.session.commit()

        response = self.client.get('/v1/posts/')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        items = response_data['items']
        self.assertEqual(len(items), 1)
        title = items[0]["title"]
        self.assertEqual(title, "title")

    def test_login(self):
        password_hash = generate_password_hash("password").decode("utf-8")
        user = User(name='testuser', email='testuser@test.com', password=password_hash)
        db.session.add(user)
        db.session.commit()

        login_data = {'email': 'testuser@test.com', 'password': 'password'}
        login_response = self.client.post('/v1/auth/login', json=login_data)
        self.assertEqual(login_response.status_code, 200)
    
    def test_get_user_profile(self):
        password_hash = generate_password_hash("password").decode("utf-8")
        user = User(name='testuser', email='testuser@test.com', password=password_hash)
        db.session.add(user)
        db.session.commit()

        login_data = {'email': 'testuser@test.com', 'password': 'password'}
        login_response = self.client.post('/v1/auth/login', json=login_data)
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json['access_token']

        profile_response = self.client.get('/v1/users/profile', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(profile_response.status_code, 200)
        user_data = json.loads(profile_response.data.decode('utf-8'))
        name = user_data['name']
        self.assertEqual(name, "testuser")
        
    def test_get_user_posts(self):
        password_hash = generate_password_hash("password").decode("utf-8")
        user = User(name='testuser', email='testuser@test.com', password=password_hash)
        db.session.add(user)
        db.session.commit()

        post = Post(title="title", content="content", user_id=1,)
        db.session.add(post)
        db.session.commit()

        posts_response = self.client.get('/v1/users/1/posts')
        self.assertEqual(posts_response.status_code, 200)
        posts_data = json.loads(posts_response.data.decode('utf-8'))
        first_post = posts_data[0]
        self.assertEqual(first_post["title"], "title")
        self.assertEqual(first_post["content"], "content")