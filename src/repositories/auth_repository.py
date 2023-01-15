from typing import Union

from src.interfaces.models.user import IUser
from src.interfaces.repositories.auth_repository import IAuthRepository
from src.db.models.user import User

class AuthRepository(IAuthRepository):

    def get_user_by_credentials(self, email: str, password: str) -> Union[IUser, None]:
        try:
            return User.find_by_credentials(email, password)
        except Exception as e:
            error_msg = "Exception when calling AuthRepository.get_user_by_credentials: %s\n" % e
            raise Exception(error_msg)
