from dependency_injector import containers, providers

from src.db.repositories.post_repository import PostRepository
from src.db.repositories.user_repository import UserRepository
from src.db.repositories.comment_repository import CommentRepository
from src.db.repositories.auth_repository import AuthRepository
from src.db.repositories.role_repository import RoleRepository

from src.db.services.post_service import PostService
from src.db.services.user_service import UserService
from src.db.services.auth_service import AuthService
from src.db.jwt.jwt_token_manager import JwtTokenManager

from src.tools.seed import Seed

#auth_service

class Container(containers.DeclarativeContainer):

    #config = providers.Configuration()

    post_repo = providers.Factory(PostRepository)

    post_service = providers.Factory(
        PostService, post_repo=post_repo
    )

    user_repo = providers.Factory(UserRepository)
    role_repo = providers.Factory(RoleRepository)
    auth_repo = providers.Factory(AuthRepository)

    comment_repo = providers.Factory(CommentRepository)


    user_service = providers.Factory(
        UserService,
        user_repo=user_repo,
        post_service=post_service,
    )

    jwt_token_manager = providers.Factory(JwtTokenManager)

    auth_service = providers.Factory(
        AuthService,
        auth_repos=auth_repo,
        token_manager=jwt_token_manager
    )

    seed_command = providers.Factory(
        Seed,
        role_repo=role_repo
    )
