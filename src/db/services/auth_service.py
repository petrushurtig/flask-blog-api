import datetime

from src.interfaces.models.user import IUser
from src.interfaces.repositories.auth_repository import IAuthRepository
from src.interfaces.token_manager import ITokenManager
from src.db.models.user import User

class AuthService:
    def __init__(
        self,
        auth_repo: IAuthRepository,
        token_manager: ITokenManager,
    ):
        self._auth_repo = auth_repo,
        self._token_manager = token_manager

    def login(self, email: str, password: str) -> dict:
        try:
            user: IUser = self._auth_repo.get_user_by_credential(email, password)

            if not user:
                raise Exception("User not found")

            issued_at = datetime.datetime.now(tz=datetime.timezone.utc)
            access_token_expries = issued_at + datetime.timedelta(hours=2)
            payload: dict = {
                "user_id": user.id,
                "grant_type": "ACCESS_TOKEN"
            }

            access_token = self._token_manager.encode_token(payload=payload, exp=access_token_expries, iat=issued_at)
            refresh_token_expires = issued_at + datetime.timedelta(days=14)
            refresh_token = self._token_manager.encode_token(payload=payload, exp=refresh_token_expires, iat=issued_at)

            return {
                "access_token": f"token|{access_token}",
                "refresh_token": f"token|{refresh_token}"
            }
        except Exception as e:
            error_msg = "Exception when calling AuthService.login: %s\n" % e
            raise Exception(error_msg)

    def get_user_by_token(self, token: str) -> IUser:
        try:
            token_prefix = "Bearer token|"
            if not str(token).startswith(token_prefix):
                raise Exception("Token doesn't start with Bearer token|")

            access_token = str(token).split(token_prefix)[1]
            payload = self._token_manager.decode_token(access_token)

            user: IUser = User(id=payload["user_id"], info={})

            return user
        except Exception as e:
            error_msg = "Exception when calling AuthService.get_user_by_token: %s\n" % e
            raise Exception(error_msg)