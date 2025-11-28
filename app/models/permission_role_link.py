from typing import Optional
from sqlmodel import SQLModel, Field


class PermissionRoleLink(SQLModel, table=True):
    __tablename__ = "permission_role_link"
    permission_id: Optional[int] = Field(
        default=None, foreign_key="permission_block.id", primary_key=True
    )
    role_id: Optional[int] = Field(
        default=None, foreign_key="role.id", primary_key=True
    )
