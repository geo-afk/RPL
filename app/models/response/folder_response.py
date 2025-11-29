from pydantic import BaseModel, field_validator
from datetime import datetime
import uuid
# from app.api.services.file_manager_service import normalize_and_validate_path


class FolderCreate(BaseModel):
    name: str
    path: str

    # @field_validator("path")
    # def validate_and_normalize_path(cls, v):
    #     is_valid, normalized, error = normalize_and_validate_path(v)
    #     if not is_valid:
    #         raise ValueError(error)
    #     return normalized


class FolderResponse(BaseModel):
    id: uuid.UUID
    name: str
    path: str
    os_type: str
    added_at: datetime
    last_opened_at: datetime | None

    class Config:
        from_attributes = True