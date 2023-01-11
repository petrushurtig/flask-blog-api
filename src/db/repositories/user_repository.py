import datetime

from src.interfaces.models.user import IUser
from src.db.config.db import db
from src.db.dbmodels.user import User
from src.interfaces.repositories.user_repository import IUserRepository

class UserRepository(IUserRepository):
    
    def get_by_id(self, user_id: int) -> IUser:
        return User.get_user_by_id(user_id)

    def get_all_users(self) -> "list[IUser]":
        return User.get_all_users()

    def create_user(self, user_data: dict) -> IUser:
        user = User(
            name = user_data["name"],
            email = user_data["email"],
            password = user_data["password"]
        )

        user.created_at = datetime.datetime.now(tz=datetime.timezone.utc)
        user.create()

        return user