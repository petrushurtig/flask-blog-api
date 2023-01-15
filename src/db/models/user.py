import datetime
from marshmallow import fields, Schema
from flask_bcrypt import check_password_hash

from src.db.models.user_roles import user_roles
from src.db.config.db import db
from app import app

class User(db.Model):
    __tablename__= 'users'

    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now(tz=datetime.timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=datetime.datetime.now(tz=datetime.timezone.utc))
    posts = db.relationship('Post', backref='users', lazy=True, cascade="all, delete-orphan")
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref("users", lazy=True))

    @classmethod
    def get_all_users(cls) -> "list[User]":
        return cls.query.all()

    @classmethod
    def get_user_by_id(cls, id) -> "User":
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_user_by_email(cls, email) -> "User":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_credentials(cls, email, password) -> "User":
        user = cls.query.filter_by(email=email).first()

        if user:
            correct_pass = check_password_hash(user.password, password)

            if correct_pass:
                return user

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def json(self) -> dict:
        created_at = self.created_at
        updated_at = self.updated_at

        if created_at is not None:
            created_at = created_at.isoformat()
        if updated_at is not None:
            updated_at = updated_at.isoformat()
     

        json_dict: dict = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": created_at,
            "updated_at": updated_at
        }

        if self.roles and len(self.roles):
            json_dict["roles"] = []

            for role in self.roles:
                json_dict["roles"].append(role.type.value)

        if self.posts and len(self.posts):
            json_dict["posts"] = []

            for post in self.posts:
                json_dict["posts"].append(post.json())

        return json_dict
        