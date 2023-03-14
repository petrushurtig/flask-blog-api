from src.db.config.db import db

class Tag(db.Model):
    __tablename__= 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    @classmethod
    def get_all_tags(cls) -> "list[Tag]":
        return cls.query.all()

    @classmethod
    def get_tag_by_id(cls, tag_id: int) -> "Tag":
        return cls.query.filter_by(id=tag_id).first()

    @classmethod
    def get_tag_by_name(cls, name: str) -> "Tag":
        return cls.query.filter_by(name=name).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            "id": self.id,
            "name": self.name
        }
