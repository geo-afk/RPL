from typing import Optional, List
from datetime import date
from pydantic import BaseModel

class PermissionCheck(BaseModel):
    user_roles: List[str]
    permissions: List[str]
    valid_until: Optional[date]

