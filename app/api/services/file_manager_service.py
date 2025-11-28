from app.api.database.database import DatabaseHandler, next_session
from app.models.auth_models import UserAuth
from sqlalchemy.orm import Session

from app.models.permission import PermissionBlock
from app.models.user import User
from typing import List, Any

session: Session = next_session
user_auth_db = DatabaseHandler(session, UserAuth)
user_db = DatabaseHandler(session, User)



def folders_for_user(user_id: int) -> list[Any] | None:

    user_auth: UserAuth = user_auth_db.get(user_id)
    resources = []

    if not user_auth:
        return resources

    user_details_id = user_auth.details_id

    user: User = user_db.get(user_details_id)

    if not user:
        return resources



    user_roles = user.roles

    for role in user_roles:
        permissions: List[PermissionBlock] = role.permissions

        for permission in permissions:
            resource = permission.resources
            resources.append(resource)


    return resources