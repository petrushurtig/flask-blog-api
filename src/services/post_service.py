from src.interfaces.models.post import IPost
from src.interfaces.models.user import IUser
from src.interfaces.services.post_service import IPostService
from src.interfaces.repositories.post_repository import IPostRepository
from src.interfaces.repositories.tag_repository import ITagRepository
from src.services.comment_service import CommentService

from app import app

class PostService(IPostService):
    def __init__(
        self, 
        post_repo: IPostRepository,
        comment_service: CommentService,
        tag_repo: ITagRepository,
    ):
        self._post_repo = post_repo
        self._comment_service = comment_service
        self._tag_repo = tag_repo

    def get_post_by_id(self, post_id: int) -> IPost:
        return self._post_repo.get_post_by_id(post_id)
    
    def increment_views(self, post_id: int):
        try:
            self._post_repo.increment_views(post_id)
        except Exception as e:
            msg = ("Error when calling PostService.increment_views: %\n" % e)
            raise Exception(msg)


    def get_all_posts(self, page:int, per_page:int) -> "list[dict]":
        posts = self._post_repo.get_all_posts(page, per_page)

        return posts

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

    def get_posts_by_tag(self, tag: str) -> "list[dict]":
        try:
            posts: "list[IPost]" = self._post_repo.get_posts_by_tag(tag)
            posts_list: "list[dict]" = []

            for post in posts:
                posts_list.append(post.json())

            return posts_list
        except Exception as e:
            msg = ("Error when calling PostService.get_posts_by_tag: %\n" % e)
            raise Exception(msg)

    def get_user_posts(self, user_id: int) -> "list[dict]":
        return self._post_repo.get_posts_by_user_id(user_id)

    def create_post(self, user_id: str, post_data: dict) -> IPost:
        
        if "title" not in post_data:
            raise Exception("Title is required")

        if "content" not in post_data:
            raise Exception("Content is required")

        if "tags" in post_data:
            request_tags = post_data["tags"]

            post_tags = []

            for tag_name in request_tags:
                existing_tag = self._tag_repo.get_tag_by_name(tag_name)

                if existing_tag:
                    post_tags.append(existing_tag)

                if not existing_tag:
                    new_tag = self._tag_repo.create_tag(tag_name)
                    post_tags.append(new_tag)

            post_data["tags"] = post_tags

        post: IPost = self._post_repo.create_post(user_id, post_data)
        
        return post

    def update_post(self, post_id: int, post_data: dict) -> IPost:
        try:

            if "tags" in post_data:
                request_tags = post_data["tags"]

                post_tags = []

                for tag_name in request_tags:
                    existing_tag = self._tag_repo.get_tag_by_name(tag_name)

                    if existing_tag:
                        post_tags.append(existing_tag)

                    if not existing_tag:
                        new_tag = self._tag_repo.create_tag(tag_name)
                        post_tags.append(new_tag)

                    post_data["tags"] = post_tags


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
