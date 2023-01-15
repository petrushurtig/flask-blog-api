from dependency_injector import containers, providers

from src.repositories.post_repository import PostRepository
from src.repositories.user_repository import UserRepository
from src.repositories.comment_repository import CommentRepository
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RoleRepository

from src.services.post_service import PostService
from src.services.user_service import UserService
from src.services.auth_service import AuthService
from src.services.comment_service import CommentService
from src.web.jwt.jwt_token_manager import JwtTokenManager

from src.common.seed import Seed

#auth_service

class Container(containers.DeclarativeContainer):

    #config = providers.Configuration()

    post_repo = providers.Factory(PostRepository)

    user_repo = providers.Factory(UserRepository)
    role_repo = providers.Factory(RoleRepository)
    auth_repo = providers.Factory(AuthRepository)

    comment_repo = providers.Factory(CommentRepository)

    comment_service = providers.Factory(
        CommentService,
        comment_repo=comment_repo,
    )

    post_service = providers.Factory(
        PostService, 
        post_repo=post_repo,
        comment_service=comment_service,
    )

    user_service = providers.Factory(
        UserService,
        user_repo=user_repo,
        post_service=post_service,
        comment_service=comment_service,
    )

    jwt_token_manager = providers.Factory(JwtTokenManager)

    auth_service = providers.Factory(
        AuthService,
        auth_repo=auth_repo,
        token_manager=jwt_token_manager
    )

    seed_command = providers.Factory(
        Seed,
        role_repo=role_repo
    )
