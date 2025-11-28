from typing import List, Dict, Any, Optional
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON, Enum as SQLAlchemyEnum


class ResourceType(str, Enum):
    API = "api"
    FOLDER = "folder"
    DATABASE = "database"


class Resource(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    path: str = Field(index=True)

    resource_type: ResourceType = Field(
        sa_column=Column(SQLAlchemyEnum(ResourceType, native_enum=False, length=50), nullable=False)
    )

    meta: Dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column("metadata", JSON)
    )

    parent_id: Optional[int] = Field(default=None, foreign_key="resource.id")
    line_number: int = 0

    parent: Optional["Resource"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "Resource.id"}
    )
    children: List["Resource"] = Relationship(back_populates="parent")
