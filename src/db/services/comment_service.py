

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

    def create_comment(self, comment_data: dict) -> "list[IComment]":
        comment: IComment = self._comment_repo.create_comment(comment_data)

        return comment

    

        