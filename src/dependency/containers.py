from dependency_injector import containers, providers

from src.db.repositories.post_repository import PostRepository
from src.db.repositories.user_repository import UserRepository
from src.db.repositories.comment_repository import CommentRepository

from src.db.services.post_service import PostService

#auth_service

class Container(containers.DeclarativeContainer):

    #config = providers.Configuration()

    post_repo = providers.Factory(PostRepository)

    post_service = providers.Factory(
        PostService, post_repo=post_repo
    )

    user_repo = providers.Factory(UserRepository)

    comment_repo = providers.Factory(CommentRepository)
