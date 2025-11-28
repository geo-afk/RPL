from datetime import datetime
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.api.services.auth_service import (
    user_details_handler,
    create_access_token,
    authenticate_user,
    user_handler,
    user_auth_handler,
    hash_password,
    DatabaseHandler,
    token_handler,
    get_user_by_username,
    get_user_details
)
from app.models.auth_models import Token, UserAuth, UserDetails
from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User
from starlette import status

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


class UserAuthResponse(BaseModel):
    message: str



class UserRegisterRequest(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: str
    password: str
    username: str




@auth_router.post(
    "/register/auth",
    status_code=status.HTTP_201_CREATED,
    response_model=Token,
    summary="Register user with authentication",
    description="Create user authentication credentials"
)
async def create_user_auth(request: UserRegisterRequest, db: DatabaseHandler[UserAuth] = Depends(user_auth_handler)):

    user_auth_construct = UserAuth(
        username=request.username,
        password_hash = hash_password(request.password)
    )

    saved_auth = db.create(user_auth_construct)

    user_db = user_handler()
    user_from_db = user_db.get(request.user_id)

    user_details_construct = UserDetails(
        email = request.email,
        first_name = request.first_name,
        last_name = request.last_name,
        auth = saved_auth,
        user = user_from_db
    )

    user_details_db = user_details_handler()
    user_details_db.create(user_details_construct)

    token = create_access_token(saved_auth.username, request.user_id)

    return Token(access_token=token, token_type="bearer")






@auth_router.post("/login", response_model=Token)
async def login_with_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DatabaseHandler[UserAuth] = Depends(token_handler)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid User credentials")

    token = create_access_token(user.username, user.id)
    return Token(access_token=token, token_type="bearer")




@auth_router.get(
    "/check/username",
    response_model=int,
    summary="check if username is available.",
    description="Check if username exists and if the user account is already setup.",
)
async def check_username(username: str, db: DatabaseHandler[User] = Depends(user_handler)):
    user = await get_user_by_username(username, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid: Username not found")

    user_details = get_user_details(user)

    if user_details:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid: User already setup")


    return user.id



#
# # routes/auth.py
# @router.get("/check-username")
# async def check_username(username: str, db: Session = Depends(get_db)):
#     exists = db.exec(select(UserAuth).where(UserAuth.username == username)).first()
#     return {"available": not bool(exists)}
#
# @router.post("/signup")
# async def signup(user_data: SignupSchema, db: Session = Depends(get_db)):
#     # Check if username or email exists...
#     # Hash password, create UserDetails + UserAuth records
#     # Return success

# @auth_router.get("/", status_code=status.HTTP_200_OK)
# async def user_auth(user: user_dependency):
#
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid User credentials, Auth Failed")
#
#     return {"User", user}