from datetime import datetime, timedelta
from sqlmodel import select
from sqlmodel.ext.asyncio.session import Session
from app.api.mock_server.rest.mock_models import ProjectStatus, TaskStatus, TaskPriority, Project, Task

# -------------------
# MOCK DATA
# -------------------
mock_projects = [
    {"name": "Website Redesign", "description": "New marketing site with animations", "status": ProjectStatus.active},
    {"name": "Mobile App MVP", "description": "Launch iOS & Android apps", "status": ProjectStatus.active},
    {"name": "Q4 Marketing Campaign", "description": "Black Friday + Christmas push", "status": ProjectStatus.completed},
    {"name": "Backend Migration", "description": "Move from Flask to FastAPI", "status": ProjectStatus.archived},
]

mock_tasks = [
    ("Design homepage mockup", "Create 3 variants in Figma", TaskStatus.in_progress, TaskPriority.high, 1),
    ("Implement authentication", "Add JWT + social login", TaskStatus.todo, TaskPriority.urgent, 2),
    ("Write API documentation", "Use FastAPI + Redoc", TaskStatus.done, TaskPriority.medium, 1),
    ("Fix payment gateway bug", "Stripe webhook failing", TaskStatus.review, TaskPriority.urgent, 2),
    ("Launch Instagram ads", "Target tech audience", TaskStatus.done, TaskPriority.high, 3),
    ("Database optimization", "Add indexes to users table", TaskStatus.todo, TaskPriority.medium, 4),
]


def seed(db: Session) -> bool:
    result = db.exec(select(Project))
    if result.first():
        return False   # already seeded

    projects: list[Project] = []

    for p in mock_projects:
        project = Project(**p)
        db.add(project)
        projects.append(project)

    db.flush()

    for title, desc, status, priority, proj_idx in mock_tasks:
        task = Task(
            title=title,
            description=desc,
            status=status,
            priority=priority,
            project_id=projects[proj_idx - 1].id,
            due_date=(
                datetime.utcnow() + timedelta(days=(proj_idx % 3) * 7)
                if priority != TaskPriority.low
                else None
            ),
        )
        db.add(task)

    db.commit()
    return True

