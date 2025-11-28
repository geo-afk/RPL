from typing import Optional, List
from sqlmodel import SQLModel, Field, Column, JSON, Relationship
from app.models.permission_role_link import PermissionRoleLink


class PermissionBlock(SQLModel, table=True):
    __tablename__ = "permission_block"
    id: Optional[int] = Field(default=None, primary_key=True)
    actions: List[str] = Field(sa_column=Column(JSON))
    resources: List[str] = Field(sa_column=Column(JSON))
    conditions: Optional[str] = None

    roles: List["Role"] = Relationship(
        back_populates="permissions",
        link_model=PermissionRoleLink
    )

    def __str__(self):
        cond = f" IF {self.conditions}" if self.conditions else ""
        return f"{self.actions} on {self.resources}{cond}"
