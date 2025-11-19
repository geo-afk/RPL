from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import Optional


# class TokenPayload(BaseModel):
#     """Decoded token payload."""
#     sub: str  # subject (username)
#     exp: datetime  # expiration
#     iat: datetime  # issued at
#     type: str  # token type
#
#
# class RefreshTokenModel(Base):
#     """
#     Store refresh tokens for token rotation strategy.
#     Allows revoking specific tokens.
#     """
#     __tablename__ = "refresh_tokens"
#
#     id = Column(String, primary_key=True)
#     user_id = Column(String, nullable=False, index=True)
#     token = Column(String, unique=True, nullable=False)
#     expires_at = Column(DateTime, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     revoked = Column(Boolean, default=False)
#

class Token(SQLModel, table=False):
    access_token: str
    token_type: str

class UserDetails(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = Field(default=True)
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    auth: Optional["UserAuth"] = Relationship(back_populates="details")


class UserAuth(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password_hash: str


    details_id: Optional[int] = Field(default=None, foreign_key="user_details.id", unique=True)
    details: Optional[UserDetails] = Relationship(back_populates="auth")
