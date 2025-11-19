from typing import List, Dict, Any, Optional
from sqlmodel import SQLModel, Field
from app.models.role import Role
from app.models.permission import PermissionBlock


class User(SQLModel, table=True):
    """Represents a user with roles and attributes."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    roles: List[str] = Field(default_factory=list, sa_column_kwargs={"type_": "jsonb"})
    attributes: Dict[str, Any] = Field(default_factory=dict, sa_column_kwargs={"type_": "jsonb"})
    valid_from: Optional[str] = None
    valid_until: Optional[str] = None
    line_number: int = 0

    def get_all_permissions(self, role_registry: Dict[str, Role]) -> List[PermissionBlock]:
        """Get all permissions from assigned roles."""
        all_perms = []
        for role_name in self.roles:
            if role_name in role_registry:
                all_perms.extend(role_registry[role_name].get_all_permissions(role_registry))
        return all_perms

    def __str__(self):
        validity = ""
        if self.valid_from or self.valid_until:
            validity = f" (valid: {self.valid_from} - {self.valid_until})"
        return f"User({self.name}, roles={self.roles}{validity})"