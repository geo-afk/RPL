from typing import List, Optional
from fastapi import APIRouter, Query, Depends, HTTPException, status
from sqlmodel import Session, select

from app.api.mock_server.rest.mock_models import Project, Task, TaskStatus
from app.api.mock_server.rest.mock_service import get_db
from app.api.mock_server.rest.seed_data import seed
from app.api.mock_server.rest.response_models import (
    ProjectCreate, ProjectUpdate, TaskCreate,
    TaskUpdate, HealthResponse,
    DeleteResponse, TaskStatusResponse
)


def ensure_seeded():
    seeded = seed(next(get_db()))
    if seeded:
        print("Database seeded for router!")
    else:
        print("Database already initialized.")


mock_router = APIRouter(
    prefix="/mock",
    tags=["Services"],
    dependencies=[Depends(ensure_seeded)],
)


# ================= HEALTH =================

@mock_router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Check service health",
    description="Returns the health status of the Mock API including client_db connectivity."
)
async def health():
    return HealthResponse(status="ok", database="connected", data="real")


# ================= PROJECTS =================

@mock_router.get(
    "/projects",
    response_model=List[Project],
    status_code=status.HTTP_200_OK,
    summary="List all projects",
    description="Returns a list of all projects ordered by creation."
)
def list_projects(db: Session = Depends(get_db)):
    query = select(Project).order_by(Project.id)

    return db.exec(query).all()

    # result = db.exec(Project.__table__.select().order_by(Project.id))
    # return result.scalars().all()


@mock_router.post(
    "/projects",
    response_model=Project,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
    description="Creates a new project and stores it in the client_db."
)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    db_project = Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@mock_router.get(
    "/projects/{project_id}",
    response_model=Project,
    status_code=status.HTTP_200_OK,
    summary="Get a single project",
    description="Fetch a project using its unique project ID."
)
def get_project(project_id: int, db: Session = Depends(get_db)):
    result = db.get(Project, project_id)
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")
    return result


@mock_router.put(
    "/projects/{project_id}",
    response_model=Project,
    status_code=status.HTTP_200_OK,
    summary="Update a project",
    description="Updates an existing project by replacing its fields."
)
def update_project(project_id: int, project: ProjectUpdate, db: Session = Depends(get_db)):
    db_project = db.get(Project, project_id)
    if not db_project:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")
    for key, value in project.model_dump(exclude_unset=True).items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    return db_project


@mock_router.delete(
    "/projects/{project_id}",
    response_model=DeleteResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete a project",
    description="Deletes a project permanently from the system."
)
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = await db.get(Project, project_id)
    if not db_project:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")
    db.delete(db_project)
    db.commit()
    return DeleteResponse(detail="Project deleted successfully")



@mock_router.get(
    "/tasks",
    response_model=List[Task],
    status_code=status.HTTP_200_OK,
    summary="List all tasks",
    description="Returns tasks and supports filtering by status, priority, or project ID."
)
def list_tasks(
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None, description="Filter by task status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    project_id: Optional[int] = Query(None, description="Filter by project ID")
):
    query = Task.__table__.select()
    if status:
        query = query.where(Task.status == status)
    if priority:
        query = query.where(Task.priority == priority)
    if project_id:
        query = query.where(Task.project_id == project_id)
    return db.exec(query.order_by(Task.id)).all()



@mock_router.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Creates a task and assigns it to a project."
)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@mock_router.get(
    "/tasks/{task_id}",
    response_model=Task,
    status_code=status.HTTP_200_OK,
    summary="Get a task",
    description="Returns a task by its ID."
)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found")
    return task


@mock_router.put(
    "/tasks/{task_id}",
    response_model=Task,
    status_code=status.HTTP_200_OK,
    summary="Update a task",
    description="Updates a task fully."
)
async def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = await db.get(Task, task_id)
    if not db_task:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found")
    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task


@mock_router.delete(
    "/tasks/{task_id}",
    response_model=DeleteResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete a task",
    description="Deletes a task permanently."
)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = await db.get(Task, task_id)
    if not db_task:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found")
    db.delete(db_task)
    db.commit()
    return DeleteResponse(detail="Task deleted successfully")


@mock_router.patch(
    "/tasks/{task_id}/status",
    response_model=TaskStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Update task status",
    description="Updates a task status value (Todo / In Progress / Completed)."
)
async def update_task_status(task_id: int, task_status: TaskStatus, db: Session = Depends(get_db)):
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found")
    task.status = task_status
    db.commit()
    db.refresh(task)
    return TaskStatusResponse(id=task.id, status=task.status)
