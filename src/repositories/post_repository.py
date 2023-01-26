import datetime

from src.interfaces.models.post import IPost
from src.interfaces.repositories.post_repository import IPostRepository
from src.db.config.db import db
from src.db.models.post import Post
from src.db.models.tag import Tag

class PostRepository(IPostRepository):

    def get_post_by_id(self, post_id: int) -> IPost:
        return Post.get_post_by_id(post_id)
    
    def increment_views(self, post_id: int):
        post = self.get_post_by_id(post_id)
        post.views += 1
        db.session.commit()

    def get_all_posts(self, page: int, per_page: int):
        return Post.get_all_posts(page, per_page)

    def get_posts_by_user_id(self, user_id: int) -> "list[IPost]":
        return Post.get_posts_by_user_id(user_id)

    def get_posts_by_tag(self, tag: str) -> "list[IPost]":
        return Post.get_posts_by_tag(tag)

    def create_post(self, user_id: int, post_data: dict) -> IPost:

        post = Post(
            title=post_data["title"],
            content=post_data["content"],            
        )

        if "tags" in post_data:
            post.tags = post_data["tags"]

        post.user_id = user_id,
        post.created_at = datetime.datetime.now(tz=datetime.timezone.utc)
        
        post.save()

        return post

    def update_post(self, post_id: int, post_data: dict) -> IPost:
        try:
            post: IPost = Post.get_post_by_id(post_id)

            if not post:
                raise Exception("Post not found")

            if "title" in post_data:
                post.title = post_data["title"]

            if "content" in post_data:
                post.content = post_data["content"]

            if "tags" in post_data:
                post.tags = post_data["tags"]

            post.updated_at = datetime.datetime.now(tz=datetime.timezone.utc)

            db.session.commit()

            return post
        
        except Exception as e:
            msg = ("Exception when calling PostRepo.update_post %s\n" % e)
            raise Exception(msg)

    def delete_post(self, post_id: int) -> bool:
        try:
            post: Post = Post.get_post_by_id(post_id)

            if not post:
                raise Exception("Post not found")

            post.delete()

            return True

        except Exception as e:
            msg = ("Exception when calling PostRepo.delete_post %s\n" % e)
            raise Exception(msg)
        

    def _get_tags_from_post_data(self, post_data: dict) -> "list[Tag]":
        tags: "list[Tag]" = []

