from flask_bcrypt import generate_password_hash

from src.db.enums.role_type import RoleType
from src.interfaces.models.user import IUser
from src.interfaces.models.post import IPost
from src.interfaces.models.comment import IComment
from src.interfaces.repositories.user_repository import IUserRepository
from src.interfaces.services.post_service import IPostService
from src.interfaces.services.comment_service import ICommentService
from src.common.exceptions.request_data_exception import RequestDataException
from src.common.exceptions.user_not_found_exception import UserNotFoundException


class UserService:
    _user_repo: IUserRepository
    _post_service: IPostService
    _comment_service: ICommentService

    def __init__(
        self, 
        user_repo: IUserRepository,
        post_service: IPostService,
        comment_service: ICommentService
    ):
        self._user_repo = user_repo
        self._post_service = post_service
        self._comment_service = comment_service


    def find_by_id(self, user_id: int) -> IUser:
        return self._user_repo.get_by_id(user_id)

    def get_user_by_email(self, email: str) -> IUser:
        return self._user_repo.get_user_by_email(email)

    def get_all_users(self) -> "list[dict]":
        users: "list[IUser]" = self._user_repo.get_all_users()
        users_list: "list[dict]" = []

        for u in users:
            users_list.append(u.json())
            
        return users_list

    def create_user(self, user_data: dict) -> IUser:

        if "email" not in user_data:
            raise RequestDataException("Email is required")
        
        if "password" not in user_data:
            raise RequestDataException("password is required")
        
        if "name" not in user_data:
            raise RequestDataException("name is required")
        
        email_exists = self._user_repo.get_user_by_email(user_data["email"])

        if email_exists:
            raise RequestDataException("Email already exists")

        name_exists = self._user_repo.get_user_by_name(user_data["name"])
        
        if name_exists:
            raise RequestDataException("Name already exists")
        
        user_data["password"] = generate_password_hash(user_data["password"]).decode("utf-8")
        user_data["roles"] = [RoleType.BASIC.value]
        user: IUser = self._user_repo.create_user(user_data)
        
        return user

    def update_user(self, user_id: int, user_data: dict) -> IUser:

        user = self._user_repo.get_by_id(user_id)

        if not user:
            raise UserNotFoundException("User not found")

        if "email" in user_data:
            email_exists = self._user_repo.get_user_by_email(user_data["email"])

            if email_exists:
                raise RequestDataException("Email already exists")
        
        if "name" in user_data:
            name_exists = self._user_repo.get_user_by_name(user_data["name"])

            if name_exists:
                raise RequestDataException("Name already exists")

        if "password" in user_data:
            user_data["password"] = generate_password_hash(user_data["password"]).decode("utf-8")

        user: IUser = self._user_repo.update_user(user_id, user_data)
        return user

    def delete_user(self, user: IUser, user_id: int = None) -> bool:
        
        if user_id:
            user_id = user_id
        else:
            user_id = user.id

        user = self._user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException("User not found")

        #delete user's posts

        posts: "list[IPost]" = self._post_service.get_user_posts(user.id)

        if posts and len(posts):
            for post in posts:
                if not self._post_service.delete_post(post.id):
                    raise Exception("Couldn't delete posts when deleting user")

        #delete user's comments

        comments: "list[IComment]" = self._comment_service.get_user_comments(user.id)

        if comments and len(comments):
            for comment in comments:
                if not self._comment_service.delete_comment(comment.id):
                    raise Exception("Couldn't delete comments when deleting user")
        
        return self._user_repo.delete_user(user_id)
""""
    def update_user(self, user_id: int, user_data: dict) -> IUser:
        
        user: IUser = self._user_repository.get_by_id(user_id)

        if not user:
            raise Exception("User not found")

"""

        