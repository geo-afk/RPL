from datetime import datetime

from pydantic import BaseModel

from app.api.database.database import DatabaseHandler
from app.api.services.auth_service import user_details_handler
from app.api.services.user_service import UserService
from fastapi import APIRouter, Depends, status

from app.models.auth_models import UserDetails
from app.models.user import User
from typing import Annotated


user_router = APIRouter(
    prefix="/user",
    tags=["User"],
)


class UserResponse(BaseModel):
    message: str

def get_user_service() -> UserService:
    return UserService()


@user_router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=list[User],
    summary="Get List of Users",
    description="Returns all users from the client_db.",
    tags=["Users"]
)
async def receive_users(
    service: Annotated[UserService, Depends(get_user_service)]
):
    return await service.get_users()



@user_router.post(
    "/save/user-details",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
    summary="Save user with authentication",
    description="Create user authentication credentials"
)
async def create_user_details(user_details: UserDetails, db: DatabaseHandler[UserDetails] = Depends(user_details_handler)):

    user_details_construct = UserDetails(
        email = user_details.email,
        first_name = user_details.first_name,
        middle_name = user_details.middle_name,
        last_name = user_details.last_name,
        is_active = user_details.is_active,
        created_at = datetime.now()
    )

    saved_user = db.create(user_details_construct)
    return {"message": f"User details created successfully {saved_user}"}



