from src.interfaces.models.user import IUser

class IUserRepository:
    def get_by_id(self, user_id: int) -> IUser:
        raise NotImplementedError

    def get_user_by_email(self, email: str) -> IUser:
        raise NotImplementedError
    
    def get_user_by_name(self, name: str) -> IUser:
        raise NotImplementedError

    def get_all_users(self) -> "list[IUser]":
        raise NotImplementedError

    def is_admin_user(self, user_id: int) -> bool:
        raise NotImplementedError

    def create_user(self, user_data: dict) -> IUser:
        raise NotImplementedError

    def update_user(self, user_id: int, user_data: dict) -> IUser:
        raise NotImplementedError

    def delete_user(self, user_id: int) -> bool:
        raise NotImplementedError