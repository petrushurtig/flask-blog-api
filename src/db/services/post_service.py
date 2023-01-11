from src.interfaces.models.post import IPost
from src.interfaces.models.user import IUser
from src.interfaces.services.post_service import IPostService
from src.interfaces.repositories.post_repository import IPostRepository

from app_source import app

class PostService(IPostService):
    def __init__(
        self, post_repo: IPostRepository
    ):
        self._post_repo = post_repo

    def get_post_by_id(self, post_id: int) -> IPost:
        return self._post_repo.get_post_by_id(post_id)

    def get_all_posts(self) -> "list[dict]":
        posts: "list[IPost]" = self._post_repo.get_all_posts()
        posts_list: "list[dict]" = []
        
        for p in posts:
            posts_list.append(p.json())

        return posts_list

    def create_post(self, user_id: str, post_data: dict) -> IPost:
        post: IPost = self._post_repo.create_post(user_id, post_data)
        
        return post

    def update_post(self, post_id: int, post_data: dict) -> IPost:
        try:
            post: IPost = self._post_repo.update_post(post_id, post_data)

            return post
        except Exception as e:
            msg = ("Error when calling PostService.update_post: %\n" % e)
            raise Exception(msg)

    def delete_post(self, post_id: int, user: IUser) -> bool:
        try:
            #delete post comments

            self._post_repo.delete_post(post_id)

            return True
        except Exception as e:
            msg = ("Error when calling PostService.delete_post: %\n" % e)
            raise Exception(msg)
