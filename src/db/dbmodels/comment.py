import datetime
from marshmallow import fields, Schema

from src.db.config.db import db

class Comment(db.Model):
    __tablename__= 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    @classmethod
    def get_all_comments(cls) -> "list[Comment]":
        return cls.query.all()

    @classmethod
    def get_comment_by_id(cls, comment_id: int) -> "Comment":
        return cls.query.filter_by(id=comment_id).first()

    @classmethod
    def get_comments_by_post_id(cls, post_id: int) -> "list[Comment]":
        return cls.query.filter_by(post_id=post_id).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id,
            "content": self.content,
            "created_at": self.created_at
        }