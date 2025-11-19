from typing import Optional, List, Dict, Any
from sqlmodel import SQLModel, Field, Relationship, Column, JSON


class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

    permissions: List[int] = Field(
        sa_column=Column(JSON),  # store PermissionBlock IDs or dicts
        default=[]
    )

    parent_role_id: Optional[int] = Field(default=None, foreign_key="role.id")
    parent_role: Optional["Role"] = Relationship(back_populates="children")
    children: List["Role"] = Relationship(back_populates="parent_role")

    attributes: Dict[str, Any] = Field(sa_column=Column(JSON), default={})
    line_number: int = 0

    def get_all_permissions(self, registry: Dict[str, "Role"]):
        # cannot access DB here; use stored registry (same as your original)
        perms = self.permissions.copy()
        if self.parent_role:
            perms.extend(self.parent_role.permissions)
        return perms

    def __str__(self):
        parent = f" extends {self.parent_role.name}" if self.parent_role else ""
        return f"Role({self.name}{parent}, {len(self.permissions)} permissions)"
