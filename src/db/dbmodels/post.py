import datetime
from marshmallow import fields, Schema

from src.db.config.db import db

class Post(db.Model):
    __tablename__= 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    comments = db.relationship('Comment', backref='posts', lazy=True)

    @staticmethod
    def get_all_posts():
        posts = Post.query.all()
        return [post.json() for post in posts]

    @staticmethod
    def get_post_by_id(id):
        return Post.query.get(id)

    @staticmethod
    def get_posts_by_user_id(user_id):
        return Post.query.filter_by(user_id=user_id).all()

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

    def json(self):
        created_at = self.created_at
        updated_at = self.updated_at

        if created_at is not None:
            created_at = created_at.isoformat()
        if updated_at is not None:
            updated_at = updated_at.isoformat()

        json_dict = {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "content": self.content,
            "created_at": created_at,
            "updated_at": updated_at
        }

        if self.comments and len(self.comments):
            json_dict["comments"] = []

            for comment in self.comments:
                json_dict["comments"].append(comment.json())

        return json_dict