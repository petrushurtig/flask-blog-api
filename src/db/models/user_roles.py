from src.db.config.db import db


user_roles = db.Table('user_roles',
                      db.Column('user_id', db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE')),
                      db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))
