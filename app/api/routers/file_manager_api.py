from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from starlette import status
from app.api.database.database import get_session
from app.api.services.file_manager_service import folders_for_user,  get_folders, add_folders
from app.api.services.auth_service import get_current_user
from app.models.response.folder_response import FolderResponse, FolderCreate


file_manager_router = APIRouter(
    prefix="/file-manager",
    tags=["file-manager"],
)


@file_manager_router.get(
    path="/folder",
    status_code=status.HTTP_200_OK,
    response_model=FolderResponse,
    summary="Get Folders",
    description="Retrieve list of folders for the current user")
async def get_folder(token: str):
    user_details: Dict[str, Any] = await get_current_user(token)

    if not user_details:
        return {"folders": []}

    user_id = user_details.get("id")
    folders = folders_for_user(user_id)

    if folders == []:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No folders found for the user.")
    return folders



@file_manager_router.get("/folders", response_model=List[FolderResponse])
def list_folders(session: Session = Depends(get_session)):
    return get_folders(session)



@file_manager_router.post("/folders", response_model=FolderResponse, status_code=201)
def add_folder(
    folder: FolderCreate,
    session: Session = Depends(get_session)
):
    return add_folders(session, folder)

