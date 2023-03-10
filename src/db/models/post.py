import datetime

from src.db.config.db import db
from src.db.models.post_tags import post_tags
from src.db.models.tag import Tag

class Post(db.Model):
    __tablename__= 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now(tz=datetime.timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=datetime.datetime.now(tz=datetime.timezone.utc))
    comments = db.relationship('Comment', backref='posts', lazy=True, cascade="all, delete-orphan")
    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy=True))

    @classmethod
    def get_post_by_id(cls, post_id: int) -> "Post":
        return cls.query.filter_by(id=post_id).first()

    @classmethod
    def get_all_posts(cls, page: int, per_page: int) -> "list[Post]":
        return cls.query.paginate(page, per_page)

    @classmethod
    def get_posts_by_user_id(cls, user_id: int) -> "list[Post]":
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_posts_by_tag(cls, tag: str) -> "list[Post]":
        return cls.query.filter(cls.tags.any(Tag.name == tag)).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def json(self, links: bool = False) -> dict:
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

        if links:
            json_dict["links"] = [
            {"rel": "comments", "href": f"/v1/posts/{self.id}/comments"},
            {"rel": "tags", "href": f"/v1/posts/{self.id}/tags"}]

        if self.comments and len(self.comments) and not links:
            json_dict["comments"] = []

            for comment in self.comments:
                json_dict["comments"].append(comment.json())
    
        if self.tags and len(self.tags) and not links:
            json_dict["tags"] = []

            for tag in self.tags:
                json_dict["tags"].append(tag.json())

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