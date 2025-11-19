from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.api.services.user_service import (
    create_access_token,
    authenticate_user,
    user_auth_handler,
    user_dependency,
    DatabaseHandler,
    bcrypt_context,
    token_handler
)
from app.models.auth_models import Token, UserAuth
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    "/register/user",
    status_code=status.HTTP_201_CREATED,
    response_model=map,
    summary="Register user with authentication",
    description="Create user authentication credentials"
)
async def create_user_auth(user_auth: UserAuth, db: DatabaseHandler[UserAuth] = Depends(user_auth_handler)):

    user_auth_construct = UserAuth(
        username=user_auth.username,
        password_hash = bcrypt_context.hash(user_auth.password)
    )

    saved_user = db.create(user_auth_construct)
    return {"message": f"User authentication created successfully {saved_user}"}




@router.post("/login", response_model=Token)
async def login_with_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DatabaseHandler[UserAuth] = Depends(token_handler)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid User credentials")

    token = create_access_token(user.username, user.id)
    return {'access_token': token, 'token_type': 'bearer'}


@router.get("/", status_code=status.HTTP_200_OK)
async def user_auth(user: user_dependency, db: DatabaseHandler[UserAuth] = Depends(token_handler)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid User credentials, Auth Failed")

    return {"User", user}