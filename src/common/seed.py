from src.interfaces.repositories.role_repository import IRoleRepository
from src.interfaces.command import ICommand

class Seed(ICommand):
    _role_repo: IRoleRepository

    def __init__(
        self,
        role_repo: IRoleRepository
    ):
        self._role_repo = role_repo

    def execute(self, **kwargs) -> None:
        print("\nSeeding...")
        self._role_repo.init_roles()

        print("Seeding done\n")