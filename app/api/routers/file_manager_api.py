from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette import status

from app.api.services.file_manager_service import folders_for_user
from app.api.services.auth_service import get_current_user

file_manager_router = APIRouter(
    prefix="/file-manager",
    tags=["file-manager"],
)

class FolderResponse(BaseModel):
    folders: list[str]


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
