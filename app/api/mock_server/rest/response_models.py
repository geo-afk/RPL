# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import datetime

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: Optional[Literal["active", "archived", "completed"]] = "active"

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Literal["active", "archived", "completed"]] = None

class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[Literal["todo", "in_progress", "review", "done"]] = "todo"
    priority: Optional[Literal["low", "medium", "high", "urgent"]] = "medium"
    due_date: Optional[datetime] = None
    project_id: int

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Literal["todo", "in_progress", "review", "done"]] = None
    priority: Optional[Literal["low", "medium", "high", "urgent"]] = None
    due_date: Optional[datetime] = None
    project_id: Optional[int] = None

class TaskResponse(TaskBase):
    id: int

    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    status: str
    database: str
    data: str


class DeleteResponse(BaseModel):
    detail: str


class TaskStatusResponse(BaseModel):
    id: int
    status: str
