from pydantic import BaseModel
from app.api.services.user_service import UserService
from fastapi import APIRouter, Depends, status

from app.models.request import UserDetailsSaveRequest
from app.models.user import User
from typing import Annotated
from app.api.services.auth_service import  save_users_details

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


@user_router.get(
    "/username/check/{username}",
    status_code=status.HTTP_200_OK,
    response_model=bool,
    summary="Check if username is available",
    description="Returns true if the username if in database",
    tags=["Users"]
)
async def check_username(
        username: str,
        service: Annotated[UserService, Depends(get_user_service)]
):
    user = await service.username_check(username)
    return user is not None


class UserDetailsWrapper(BaseModel):
    userDetails: UserDetailsSaveRequest


@user_router.post(
    "/save/user-details",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
    summary="Save user with authentication",
    description="Create user authentication credentials"
)
async def create_user_details(request: UserDetailsWrapper):
    print(f"Request: {request}")
    user_details = save_users_details(request.userDetails)
    response = UserResponse(message=f"User details created successfully {user_details.id}")
    return response


