from typing import Union

from src.interfaces.models.user import IUser

class IAuthRepository:
    def get_user_by_credentials(self, email: str, password: str) -> Union[IUser, None]:
        raise NotImplementedError