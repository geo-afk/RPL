from typing import List, Dict, Any, Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON


class Resource(SQLModel, table=True):
    """Represents a resource with attributes and optional hierarchy."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    attributes: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    parent_id: Optional[int] = Field(default=None, foreign_key="resource.id")
    line_number: int = 0

    parent: Optional["Resource"] = Relationship(back_populates="children")
    children: List["Resource"] = Relationship(back_populates="parent")

    def get_full_path(self) -> str:
        """Get full hierarchical path."""
        if self.parent:
            return f"{self.parent.get_full_path()}.{self.name}"
        return self.name

    def matches(self, pattern: str) -> bool:
        """Check if resource matches a pattern (supports wildcards)."""
        full_path = self.get_full_path()
        if pattern == "*":
            return True
        if pattern.endswith(".*"):
            prefix = pattern[:-2]
            return full_path.startswith(prefix)
        return full_path == pattern

    def __str__(self):
        path = self.attributes.get('path', 'N/A')
        children_info = f", {len(self.children)} children" if self.children else ""
        return f"Resource({self.name}, path={path}{children_info})"