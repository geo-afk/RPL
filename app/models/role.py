from sqlmodel import SQLModel, Field, Column, JSON, Relationship
from typing import Optional, List, Dict, Any
from app.models.permission_role_link import PermissionRoleLink
from app.models.user_role_link import UserRoleLink


class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

    permissions: List["PermissionBlock"] = Relationship(
        back_populates="roles",
        link_model=PermissionRoleLink
    )


    parent_role_id: Optional[int] = Field(default=None, foreign_key="role.id")
    parent_role: Optional["Role"] = Relationship(
        back_populates="child_roles",
        sa_relationship_kwargs={"remote_side": "Role.id"}
    )
    child_roles: List["Role"] = Relationship(
        back_populates="parent_role"
    )

    attributes: Dict[str, Any] = Field(
        sa_column=Column(JSON),
        default={}
    )

    line_number: int = 0

    users: List["User"] = Relationship(
        back_populates="roles",
        link_model=UserRoleLink
    )

    def get_all_permissions(self, registry: Dict[str, "Role"]):
        perms = list(self.permissions)

        if self.parent_role:
            perms.extend(self.parent_role.get_all_permissions(registry))

        # Deduplicate
        seen = set()
        unique = []

        for perm in perms:
            if perm not in seen:
                seen.add(perm)
                unique.append(perm)

        return unique

