from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime, UTC

class Role(BaseModel):
    """Domain model for a role."""
    name: str
    permissions: List[str]
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Admin",
                "permissions": ["read", "write", "delete"],
                "description": "Administrator role with full access"
            }
        }


class User(BaseModel):
    """Domain model for a user."""
    name: str
    role: str
    attributes: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Alice",
                "role": "Admin",
                "attributes": {
                    "department": "IT",
                    "email": "alice@example.com"
                }
            }
        }


class Resource(BaseModel):
    """Domain model for a resource."""
    name: str
    path: str
    type: Optional[str] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Config:
        json_schema_extra = {
            "example": {
                "name": "DB_Finance",
                "path": "/data/financial",
                "type": "database",
                "attributes": {
                    "sensitive": True,
                    "encryption": "AES-256"
                }
            }
        }


class PolicyRule(BaseModel):
    """Domain model for a policy rule."""
    type: Literal["ALLOW", "DENY"]
    actions: List[str]
    resource: str
    condition: Optional[str] = None
    line_number: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "type": "ALLOW",
                "actions": ["read", "write"],
                "resource": "DB_Finance",
                "condition": "time.hour > 9 AND time.hour < 17",
                "line_number": 15
            }
        }


class Policy(BaseModel):
    """Complete policy with all components."""
    id: str
    name: str
    version: str = "1.0.0"
    description: Optional[str] = None

    roles: Dict[str, Role] = Field(default_factory=dict)
    users: Dict[str, User] = Field(default_factory=dict)
    resources: Dict[str, Resource] = Field(default_factory=dict)
    rules: List[PolicyRule] = Field(default_factory=list)

    enabled: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    created_by: Optional[str] = None

