from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import Optional

class Token(SQLModel, table=False):
    access_token: str
    token_type: str




class UserDetails(SQLModel, table=True):
    __tablename__ = "user_details"
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = Field(default=True)
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    auth: Optional["UserAuth"] = Relationship(back_populates="details")
    user: Optional["User"] = Relationship(back_populates="details")


class UserAuth(SQLModel, table=True):
    __tablename__ = "user_auth"
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password_hash: str


    details_id: Optional[int] = Field(default=None, foreign_key="user_details.id", unique=True)
    details: Optional[UserDetails] = Relationship(back_populates="auth")
