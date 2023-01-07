import datetime
from marshmallow import fields, Schema

from src.db.config.db import db

class Comment(db.Model):
    __tablename__= 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

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
    def get_all_comments():
        return Comment.query.all()

    @staticmethod
    def get_comment_by_id(id):
        return Comment.query.get(id)

    @staticmethod
    def get_comments_by_post_id(post_id):
        return Comment.query.filter_by(post_id=post_id).all()

    def json(self):
        return {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at
        }