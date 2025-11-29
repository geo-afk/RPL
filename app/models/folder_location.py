from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class FolderLocation(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)                     # Display name (e.g., "Project Alpha")
    path: str = Field(unique=True, index=True)        # Normalized POSIX path
    os_type: str = Field(default="unknown")           # "Windows", "Darwin", "Linux"
    added_at: datetime = Field(default_factory=datetime.utcnow)
    last_opened_at: Optional[datetime] = None

    def is_windows(self) -> bool:
        return self.os_type == "Windows"