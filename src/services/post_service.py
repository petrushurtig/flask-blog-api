from src.interfaces.models.post import IPost
from src.interfaces.models.user import IUser
from src.interfaces.services.post_service import IPostService
from src.interfaces.repositories.post_repository import IPostRepository
from src.services.comment_service import CommentService

from app import app

class PostService(IPostService):
    def __init__(
        self, 
        post_repo: IPostRepository,
        comment_service: CommentService,
    ):
        self._post_repo = post_repo
        self._comment_service = comment_service

    def get_post_by_id(self, post_id: int) -> IPost:
        return self._post_repo.get_post_by_id(post_id)
    
    def increment_views(self, post_id: int):
        try:
            self._post_repo.increment_views(post_id)
        except Exception as e:
            msg = ("Error when calling PostService.increment_views: %\n" % e)
            raise Exception(msg)


    def get_all_posts(self) -> "list[dict]":
        posts: "list[IPost]" = self._post_repo.get_all_posts()
        posts_list: "list[dict]" = []
        
        for p in posts:
            posts_list.append(p.json())

        return posts_list

    def get_user_posts_json(self, user_id: int) -> "list[dict]":
        try:
            posts: "list[IPost]" = self._post_repo.get_posts_by_user_id(user_id)
            posts_list: "list[dict]" = []

            for post in posts:
                posts_list.append(post.json())

            return posts_list
        except Exception as e:
            app.logger.info(e)
            return "error"

    def get_user_posts(self, user_id: int) -> "list[dict]":
        return self._post_repo.get_posts_by_user_id(user_id)

    def create_post(self, user_id: str, post_data: dict) -> IPost:
        
        if "title" not in post_data:
            raise Exception("Title is required")

        if "content" not in post_data:
            raise Exception("Content is required")

        post: IPost = self._post_repo.create_post(user_id, post_data)
        
        return post

    def update_post(self, post_id: int, post_data: dict) -> IPost:
        try:
            post: IPost = self._post_repo.update_post(post_id, post_data)

            return post
        except Exception as e:
            msg = ("Error when calling PostService.update_post: %\n" % e)
            raise Exception(msg)

    def delete_post(self, post_id: int) -> bool:
        try:
            #delete post comments
            comments = self._comment_service.get_post_comments(post_id)

            if comments and len(comments):
                for comment in comments:
                    self._comment_service.delete_comment(comment.id)

            self._post_repo.delete_post(post_id)

            return True
        except Exception as e:
            msg = ("Error when calling PostService.delete_post: %\n" % e)
            raise Exception(msg)
