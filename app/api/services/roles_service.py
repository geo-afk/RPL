from app.api.database.database import DatabaseHandler, next_session
from app.models.role import Role
from typing import Sequence, List


class RoleService:
    def __init__(self):
        self.roles_db: DatabaseHandler[Role] = DatabaseHandler(next_session, Role)

    def get_roles(self) -> Sequence[Role]:
        roles: List[Role] = self.roles_db.get_all()
        return roles


