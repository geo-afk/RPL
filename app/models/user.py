from typing import List, Dict, Any, Optional
from app.models.role import Role
from app.models.user_role_link import UserRoleLink
from sqlmodel import SQLModel, Field, Relationship,  Column, JSON


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

    roles: List[Role] = Relationship(
        back_populates="users",
        link_model=UserRoleLink
    )

    attributes: Dict[str, Any] = Field(
        sa_column=Column(JSON),
        default={}
    )

    valid_from: Optional[str] = None
    valid_until: Optional[str] = None
    line_number: int = 0

    details_id: Optional[int] = Field(
        default=None,
        foreign_key="user_details.id",
        index=True,
        unique=True,
        nullable=True,
    )
    details: Optional["UserDetails"] = Relationship(back_populates="user")

    def get_all_permissions(self, role_registry):
        all_perms = []

        for role in self.roles:
            if role.name in role_registry:
                all_perms.extend(
                    role_registry[role.name].get_all_permissions(role_registry)
                )

        return all_perms

    def __str__(self):
        validity = ""
        if self.valid_from or self.valid_until:
            validity = f" (valid: {self.valid_from} - {self.valid_until})"
        return f"User({self.name}, roles={self.roles}{validity})"
