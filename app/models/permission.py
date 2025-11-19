from typing import Optional, List
from sqlmodel import SQLModel, Field, Column, JSON


class PermissionBlock(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    actions: List[str] = Field(sa_column=Column(JSON))
    resources: List[str] = Field(sa_column=Column(JSON))
    conditions: Optional[str] = None

    def __str__(self):
        cond = f" IF {self.conditions}" if self.conditions else ""
        return f"{self.actions} on {self.resources}{cond}"
