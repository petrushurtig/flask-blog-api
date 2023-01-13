from flask_bcrypt import generate_password_hash

from src.db.enums.role_type import RoleType
from src.interfaces.models.user import IUser
from src.interfaces.models.post import IPost
from src.interfaces.repositories.user_repository import IUserRepository
from src.interfaces.services.post_service import IPostService


class UserService:
    _user_repo: IUserRepository
    _post_service: IPostService

    def __init__(
        self, 
        user_repo: IUserRepository,
        post_service: IPostService,
    ):
        self._user_repo = user_repo
        self._post_service = post_service


    def find_by_id(self, user_id: int) -> IUser:
        return self._user_repo.get_by_id(user_id)

    def get_user_by_email(self, email: str) -> IUser:
        return self._user_repo.get_user_by_email(email)

    def get_all_users(self) -> "list[dict]":
        return self._user_repo.get_all_users()

    def create_user(self, user_data: dict) -> IUser:

        if "roles" not in user_data:
            user_data["roles"] = [RoleType.BASIC.value]

        if "email" not in user_data:
            raise Exception("Email is required")
        
        if "password" not in user_data:
            raise Exception("password is required")
        
   
        email = user_data["email"]
        password = user_data["password"]

        user_exist = self._user_repo.get_user_by_email(email)

        if user_exist:
            raise Exception("Email already exists")
        
        password_hash = generate_password_hash(password).decode("utf-8")
    
        user_data["passowrd"] = password_hash
        user: IUser = self._user_repo.create_user(user_data)
        
        return user

    def delete_user(self, user: IUser, user_id: int) -> bool:
        posts: "list[IPost]" = self._post_service.get_user_posts(user_id)

        if posts and len(posts):
            for post in posts:
                if not self._post_service.delete_post(post.id, user):
                    raise Exception("Couldn't delete posts when deleting user")
        
        return self._user_repository.delete_user(user_id)
""""
    def update_user(self, user_id: int, user_data: dict) -> IUser:
        
        user: IUser = self._user_repository.get_by_id(user_id)

        if not user:
            raise Exception("User not found")

"""

        