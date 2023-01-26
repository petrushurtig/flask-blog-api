from src.db.enums.role_type import RoleType
from src.interfaces.models.role import IRole

class IRoleRepository:
    def init_roles(self):
        raise NotImplementedError

    def find_by_type(self, type: RoleType) -> IRole:
        raise NotImplementedError