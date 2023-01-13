from src.interfaces.models.post import IPost
from src.interfaces.models.user import IUser

class IPostService:
    def get_post_by_id(self, post_id: int) -> IPost:
        raise NotImplementedError

    def increment_views(self, post_id: int) -> IPost:
        raise NotImplementedError

    def get_all_posts(self) -> "list[IPost]":
        raise NotImplementedError

    def get_user_posts(self) -> "list[IPost]":
        raise NotImplementedError

    def create_post(self, user_id: int, post_data: dict) -> IPost:
        raise NotImplementedError
    
    def update_post(self, post_id: int, post_data: dict) -> IPost:
        raise NotImplementedError

    def delete_post(self, post_id: int) -> bool:
        raise NotImplementedError
