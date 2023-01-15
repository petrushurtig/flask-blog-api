

from src.interfaces.models.comment import IComment
from src.interfaces.repositories.comment_repository import ICommentRepository

class CommentService:
    
    def __init__(
        self,
        comment_repo: ICommentRepository
    ):

        self._comment_repo = comment_repo

    def get_all_comments(self) -> "list[IComment]":
        comments: "list[IComment]" = self._comment_repo.get_all_comments()
        comments_list: "list[dict]" = []

        for comment in comments:
            comments_list.append(comment.json())

        return comments_list

    def get_comment_by_id(self, comment_id: int) -> IComment:
        return self._comment_repo.get_by_id(comment_id)

    def get_post_comments(self, post_id: int) -> "list[IComment]":
        comments: "list[IComment]" = self._comment_repo.get_post_comments_by_id(post_id)

        return comments

    def create_comment(self, comment_data: dict) -> "list[IComment]":
        comment: IComment = self._comment_repo.create_comment(comment_data)

        return comment

    def update_comment(self, comment_id: int, comment_data: dict) -> IComment:
        try:
            comment: IComment = self._comment_repo.update_comment(comment_id, comment_data)

            return comment
        except Exception as e:
            msg = ("Error when calling CommentService.update_comment: %s\n" % e)
            raise Exception(msg)

    def delete_comment(self, comment_id: int) -> bool:
        try:
            self._comment_repo.delete_comment(comment_id)

            return True
        except Exception as e:
            msg = ("Error when calling CommentService.delete_comment: %s\n" % e)
            raise Exception(msg)

    

        