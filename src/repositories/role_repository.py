import datetime

from src.db.enums.role_type import RoleType
from src.interfaces.models.role import IRole
from src.interfaces.repositories.role_repository import IRoleRepository
from src.db.models.role import Role

class RoleRepository(IRoleRepository):
    def init_roles(self):
        existing_admin_role: Role = Role.find_by_type(RoleType.ADMIN)

        if not existing_admin_role:
            admin_role = Role(type=RoleType.ADMIN, created_at=datetime.datetime.now(tz=datetime.timezone.utc))
            admin_role.save()

        existing_basic_role: Role = Role.find_by_type(RoleType.BASIC)

        if not existing_basic_role:
            basic_role = Role(type=RoleType.BASIC, created_at=datetime.datetime.now(tz=datetime.timezone.utc))
            basic_role.save()

    def find_by_type(self, type: RoleType) -> IRole:
        return Role.find_by_type(type)
    