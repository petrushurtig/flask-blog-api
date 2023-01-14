import datetime

from src.interfaces.models.comment import IComment
from src.interfaces.repositories.comment_repository import ICommentRepository
from src.db.config.db import db
from src.db.dbmodels.comment import Comment

class CommentRepository(ICommentRepository):
    def get_by_id(self, comment_id: int) -> IComment:
        return Comment.get_comment_by_id(comment_id)

    def get_all_comments(self) -> "list[IComment]":
        return Comment.get_all_comments()

    def create_comment(self, comment_data: dict) -> IComment:
        comment = Comment(
            content = comment_data["content"],
            post_id = comment_data["post_id"],
            user_id = comment_data["user_id"]
        )

        comment.created_at = datetime.datetime.now(tz=datetime.timezone.utc)
        comment.save()

        return comment

    def update_comment(self, comment_id: int, comment_data: dict) -> IComment:
        try:
            comment: IComment = Comment.get_comment_by_id(comment_id)

            if not comment:
                raise Exception("Comment not found")


            if "content" not in comment_data:
                raise Exception("content required")

            comment.content = comment_data["content"]
            comment.updated_at = datetime.datetime.now(tz=datetime.timezone.utc)

            db.session.commit()

            return comment
        except Exception as e:
            msg = ("Exception when calling CommentRepo.update_comment: %s\n" % e)
            raise Exception(msg)

    def delete_comment(self, comment_id: int) -> bool:
        try:
            comment: IComment = Comment.get_comment_by_id(comment_id)

            if not comment:
                raise Exception("Comment not found")

            db.session.delete(comment)
            db.session.commit()

            return comment

        except Exception as e:
            msg = ("Exception when calling CommentRepo.delete_comment: %s\n" % e)
            raise Exception(msg)