from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
import enum



class ProjectStatus(str, enum.Enum):
    active = "active"
    archived = "archived"
    completed = "completed"


class TaskPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class TaskStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    review = "review"
    done = "done"



class Project(SQLModel, table=True):
    __tablename__ = "projects"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(max_length=100, nullable=False)
    description: Optional[str] = Field(default=None)
    status: ProjectStatus = Field(default=ProjectStatus.active)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    tasks: List["Task"] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )



class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None)
    status: TaskStatus = Field(default=TaskStatus.todo)
    priority: TaskPriority = Field(default=TaskPriority.medium)
    due_date: Optional[datetime] = Field(default=None)

    project_id: int = Field(foreign_key="projects.id", nullable=False)

    project: Optional[Project] = Relationship(back_populates="tasks")
