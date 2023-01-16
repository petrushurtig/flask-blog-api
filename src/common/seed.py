from src.interfaces.repositories.role_repository import IRoleRepository
from src.interfaces.command import ICommand
from src.interfaces.repositories.user_repository import IUserRepository

class Seed(ICommand):
    _role_repo: IRoleRepository
    _user_repo: IUserRepository

    def __init__(
        self,
        role_repo: IRoleRepository,
        user_repo: IUserRepository
    ):
        self._role_repo = role_repo
        self._user_repo = user_repo

    def execute(self, **kwargs) -> None:
        print("\nSeeding...")
        self._role_repo.init_roles()
        self._user_repo.init_users()

        print("Seeding done\n")