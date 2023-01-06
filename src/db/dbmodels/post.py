import datetime
from marshmallow import fields, Schema

from src.db.config.db import db
from .comment import CommentSchema

class Post(db.Model):
    __tablename__= 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    comments = db.relationship('Comment', backref='posts', lazy=True)

    def __init__(self, data):
        self.title = data.get('title')
        self.content = data.get('content')
        self.user_id = data.get('user_id')
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.updated_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_posts():
        return Post.query.all()

    @staticmethod
    def get_post_by_id(id):
        return Post.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class PostSchema(Schema):

    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    user_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    comments = fields.Nested(CommentSchema, many=True)