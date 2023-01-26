from src.interfaces.models.comment import IComment

class ICommentRepository:
    def get_by_id(self, comment_id: int)  -> IComment:
        raise NotImplementedError

    def get_all_comments(self) -> "list[IComment]":
        raise NotImplementedError

    def get_post_comments_by_id(self, post_id: int) -> "list[IComment]":
        raise NotImplementedError
    
    def get_user_comments_by_id(self, user_id: int) -> "list[IComment]":
        raise NotImplementedError

    def create_comment(self, post_id: int, comment_data: dict) -> IComment:
        raise NotImplementedError

    def update_comment(self, comment_id: int, comment_data: dict) -> IComment:
        raise NotImplementedError
    
    def delete_comment(self, comment_id: int) -> bool:
        raise NotImplementedError