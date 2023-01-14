import datetime

from src.db.config.db import db

class Post(db.Model):
    __tablename__= 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    comments = db.relationship('Comment', backref='posts', lazy=True, cascade="all, delete-orphan")

    @classmethod
    def get_post_by_id(cls, post_id: int) -> "Post":
        return cls.query.filter_by(id=post_id).first()

    @classmethod
    def get_all_posts(cls) -> "list[Post]":
        return cls.query.all()

    @classmethod
    def get_posts_by_user_id(cls, user_id: int) -> "list[Post]":
        return cls.query.filter_by(user_id=user_id).all()

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

        json_dict = {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "content": self.content,
            "views": self.views,
            "created_at": created_at,
            "updated_at": updated_at
        }

        if self.comments and len(self.comments):
            json_dict["comments"] = []

            for comment in self.comments:
                json_dict["comments"].append(comment.json())
    
        return json_dict

""""
    def update(post_id, data):
        post = Post.query.get(post_id)

        post = Post(
        id= post_id,
        title = data["title"],
        content = data["title"],
        user_id= post.user_id,
        views= post.views,
        created_at= post.created_at,
        updated_at=datetime.datetime.now(tz=datetime.timezone.utc)
        )
        db.session.commit()
        return post

    @staticmethod
    def add_one_to_views(id):
        post = Post.query.get(id)
        post.views += 1
        db.session.commit()
        return post

    @staticmethod
    def get_posts_by_user_id(user_id):
        return Post.query.filter_by(user_id=user_id).all()
"""