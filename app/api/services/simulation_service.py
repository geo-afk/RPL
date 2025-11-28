from typing import Optional
from datetime import datetime, date

from app.api.services.auth_service import get_current_user, user_handler,role_handler
from app.models.auth_models import Token
from app.models.response.simulation_response import PermissionCheck
from app.models.role import Role
from typing import Dict, List

SUPPORTED_DATE_FORMATS = [
    "%Y-%m-%d",        # 2025-02-01
    "%d-%m-%Y",        # 01-02-2025
    "%m-%d-%Y",        # 02-01-2025
    "%Y/%m/%d",        # 2025/02/01
    "%d/%m/%Y",        # 01/02/2025
    "%m/%d/%Y",        # 02/01/2025
    "%Y.%m.%d",        # 2025.02.01
    "%d.%m.%Y",        # 01.02.2025
    "%B %d, %Y",       # February 1, 2025
    "%b %d, %Y",       # Feb 1, 2025
]

def parse_valid_until(valid_until: Optional[str]) -> Optional[date]:
    """
    Attempts to parse a date string using multiple known formats.
    Returns a date object if parsing succeeds, otherwise None.
    """

    if valid_until is None:
        return None

    valid_until = valid_until.strip()

    if not valid_until:
        return None

    for fmt in SUPPORTED_DATE_FORMATS:
        try:
            return datetime.strptime(valid_until, fmt).date()
        except ValueError:
            continue

    return None



def is_expired(valid_until_date: Optional[date]) -> bool:
    """
    Returns True if the date has passed.
    Returns False if:
      - Date is None
      - Date is today or in the future
    """

    if valid_until_date is None:
        return False

    return valid_until_date < date.today()




def check_user_permissions(token: Token):
    user_id = get_current_user(token.access_token)
    user_db = user_handler()
    user = user_db.get(user_id)

    parsed_date_string = parse_valid_until(user.valid_until)
    user_expired = is_expired(parsed_date_string)


    if not user_expired:
        return None

    role_db = role_handler(Role)

    roles: List[Role] = []
    resource_permission: Dict[str, List[str]] = {}

    for r in user.roles:
        role = role_db.get(r.id)
        roles.append(role)

        for permission in role.permissions:
            resource = permission.resources
            resource_permission[resource] = permission.actions


    return PermissionCheck(

        user_roles= [role.name for role in roles],
        permissions=[r for r in resource_permission.keys()],
        valid_until=user.parsed_date_string,
    )

