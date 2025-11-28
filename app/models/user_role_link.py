from typing import Optional
from sqlmodel import SQLModel, Field


class UserRoleLink(SQLModel, table=True):
    __tablename__ = "user_role_link"
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    role_id: Optional[int] = Field(
        default=None, foreign_key="role.id", primary_key=True
    )
