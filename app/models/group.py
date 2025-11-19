from sqlmodel import SQLModel, Field, Column, JSON
from typing import List


class Group(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str = Field(index=True, unique=True)

    members: List[str] = Field(sa_column=Column(JSON), default=[])
    roles: List[str] = Field(sa_column=Column(JSON), default=[])

    line_number: int = 0

    def __str__(self):
        return f"Group({self.name}, {len(self.members)} members, roles={self.roles})"
