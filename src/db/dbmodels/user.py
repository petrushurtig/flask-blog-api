import datetime
from marshmallow import fields, Schema
from flask_bcrypt import check_password_hash

from src.db.config.db import db, bcrypt
from app_source import app

class User(db.Model):
    __tablename__= 'users'

    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now(tz=datetime.timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=datetime.datetime.now(tz=datetime.timezone.utc))
    posts = db.relationship('Post', backref='users', lazy=True)

    def __init__(self, id, name, email, password, created_at, updated_at):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at
        
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_all_users():
        users = User.query.all()
        return [user.json() for user in users]

    def update(id, data):
        user = User.query.get(id)

        user = User(
            id = id,
            name = data["name"],
            email = data["email"],
            password = data["password"],
            created_at = user.created_at,
            updated_at=datetime.datetime.now(tz=datetime.timezone.utc)
        )
        db.session.commit()
        return user

    @staticmethod
    def get_user_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def find_by_credentials(email, password):
        user = User.query.filter_by(email=email).first()

        if user:
            app.logger.info("user found")
            correct_pass = check_password_hash(user.password, password)
            app.logger.info(correct_pass)

            if correct_pass:
                return user
            else:
                app.logger.info("pass incorrect")

    def json(self):
        created_at = self.created_at
        updated_at = self.updated_at

        if created_at is not None:
            created_at = created_at.isoformat()
        if updated_at is not None:
            updated_at = updated_at.isoformat()
     
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": created_at,
            "updated_at": updated_at
        }
"""
    def json(self):
        created_at = self.created_at
        updated_at = self.updated_at

        if created_at is not None:
            created_at = created_at.isoformat()
        if updated_at is not None:
            updated_at = updated_at.isoformat()
        
        json_dict = {
            "id": self.id,
            "name": self.name,  
            "email": self.email,  
            "password": self.password,  
            "created_at": created_at,  
            "updated_at": updated_at  
        }
        
        if self.posts and len(self.posts):
            json_dict["posts"] = []

            for post in self.posts:
                json_dict["posts"].append(post.json())
        
        return json_dict

"""