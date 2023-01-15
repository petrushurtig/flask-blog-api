import datetime

from src.db.config.db import db
from src.db.enums.role_type import RoleType

class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(RoleType), nullable=False, unique=True, default=RoleType.BASIC)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now(tz=datetime.timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=datetime.datetime.now(tz=datetime.timezone.utc))

    @classmethod
    def find_by_type(cls, type: int) -> "Role":
        return cls.query.filter_by(type=type).first()

    def save(self):
        db.session.add(self)
        db.session.commit()