from src.interfaces.models.user import IUser

class IUserRepository:
    def get_by_id(self, user_id: int) -> IUser:
        raise NotImplementedError

    def get_all_users(self) -> "list[IUser]":
        raise NotImplementedError

    def create_user(self, user_data: dict) -> IUser:
        raise NotImplementedError

    def delete_user(self, user_id: int) -> bool:
        raise NotImplementedError