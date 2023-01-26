from src.db.config.db import db

post_tags = db.Table('post_tags',
                     db.Column('post_id', db.Integer(), db.ForeignKey('posts.id', ondelete='CASCADE')),
                     db.Column('tag_id', db.Integer(), db.ForeignKey('tags.id')))