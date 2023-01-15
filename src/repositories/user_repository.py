import datetime

from src.interfaces.models.user import IUser
from src.db.config.db import db
from src.db.models.user import User
from src.db.models.role import Role
from src.db.enums.role_type import RoleType
from src.interfaces.repositories.user_repository import IUserRepository

class UserRepository(IUserRepository):
    
    def get_by_id(self, user_id: int) -> IUser:
        return User.get_user_by_id(user_id)

    def get_all_users(self) -> "list[IUser]":
        return User.get_all_users()

    def get_user_by_email(self, email: str) -> IUser:
        return User.get_user_by_email(email)

    def create_user(self, user_data: dict) -> IUser:
        user = User(
            name = user_data["name"],
            email = user_data["email"],
            password = user_data["password"]
        )

        roles: "list[Role]" = self._get_roles_from_user_data(user_data)

        if roles and len(roles):
            user.roles = roles

        user.created_at = datetime.datetime.now(tz=datetime.timezone.utc)
        user.save()

        return user

    def _get_roles_from_user_data(self, user_data: dict) -> "list[Role]":
        roles: "list[Role]" = []
        for type in user_data["roles"]:
            if not isinstance(type, RoleType):
                type = RoleType(type)

            role: Role = Role.find_by_type(type)

            if not role:
                raise Exception("role not found")

            roles.append(role)

        return roles