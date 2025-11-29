from app.api.database.database import DatabaseHandler, next_session
from app.models.auth_models import UserAuth
from pathlib import Path
from typing import Tuple
from app.models.folder_location import FolderLocation
from app.models.permission import PermissionBlock
from app.models.resource import Resource
from app.models.response.folder_response import FolderCreate
from app.models.user import User
import platform
from typing import Any, List
from fastapi import HTTPException
from sqlmodel import Session, select



session: Session = next_session
user_auth_db = DatabaseHandler(session, UserAuth)
user_db = DatabaseHandler(session, User)
resource_db = DatabaseHandler(session, Resource)



def folders_for_user(user_id: int) -> list[Any] :

    user_auth: UserAuth = user_auth_db.get(user_id)
    resource_names: List[str] = []

    if not user_auth:
        return resource_names

    user_details_id = user_auth.details_id

    user: User = user_db.get(user_details_id)

    if not user:
        return resource_names



    user_roles = user.roles

    for role in user_roles:
        permissions: List[PermissionBlock] = role.permissions

        for permission in permissions:
            resource = permission.resources

            for r in resource:
                resource_names.append(r)

    resources: List[Resource] = []



    for name in resource_names:
        query = select(Resource).where(Resource.name == name)
        resource = resource_db.session.exec(query).first()
        resources.append(resource)

    locations: List[FolderLocation] = []


    for resource in resources:
        location = resource.path

        is_valid, normalized_path, error = normalize_and_validate_path(location)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error)

        new_folder = FolderLocation(
            name=location.split("/")[-1],
            path=normalized_path,
            os_type=platform.system(),
        )

        locations.append(new_folder)



    return locations



def get_folders(db_session: Session):
    folders = db_session.exec(select(FolderLocation)).all()
    return folders



def add_folders(db_session: Session, folder:FolderCreate):
    # Double-check normalization
    is_valid, normalized_path, error = normalize_and_validate_path(folder.path)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)

    # Prevent duplicates
    existing = db_session.exec(
        select(FolderLocation).where(FolderLocation.path == normalized_path)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="This folder is already registered")

    new_folder = FolderLocation(
        name=folder.name,
        path=normalized_path,
        os_type=platform.system(),
    )
    db_session.add(new_folder)
    db_session.commit()
    db_session.refresh(new_folder)
    return new_folder



def normalize_and_validate_path(raw_path: str) -> Tuple[bool, str, str]:
    """
    Normalize path for current OS and validate it's absolute + safe.
    Returns: (is_valid, normalized_path, error_message)
    """
    if not raw_path:
        return False, "", "Path cannot be empty"

    try:

        cleaned = raw_path.strip()

        # Handle different separators
        if platform.system() == "Windows":
            # Allow both \ and /
            cleaned = cleaned.replace("/", "\\")
            if not cleaned[0].isalpha() or cleaned[1:3] != ":\\":
                return False, "", "Invalid Windows path (must be like C:\\folder)"
        else:
            # Unix-like: must start with /
            cleaned = cleaned.replace("\\", "/")
            if not cleaned.startswith("/"):
                return False, "", "Invalid Unix path (must start with /)"

        path = Path(cleaned)

        if not path.is_absolute():
            return False, "", "Path must be absolute"

        # Security: prevent traversal-like patterns
        if ".." in path.parts or path.name.startswith("."):
            return False, "", "Hidden files or parent traversal not allowed in root path"

        normalized = str(path.as_posix())  # Always store as POSIX for consistency
        return True, normalized, ""

    except Exception as e:
        return False, "", f"Invalid path format: {str(e)}"