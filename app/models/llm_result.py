from typing import Optional
from sqlmodel import SQLModel, Field


class Finding(SQLModel, table=True):
    __tablename__ = "findings"

    id: Optional[int] = Field(default=None, primary_key=True)
    line: int = Field(nullable=False)
    risk_score: int = Field(nullable=False, index=True)
    category: str = Field(nullable=False, max_length=100, index=True)
    description: str = Field(nullable=False)
    recommendation: str = Field(nullable=False)
    raw_output: Optional[str] = Field(default=None)
