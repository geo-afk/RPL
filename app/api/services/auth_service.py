from typing import Type, TypeVar

from app.api.database.database import Session, DatabaseHandler, get_session, next_session
from app.models.auth_models import UserAuth, Token, UserDetails
from app.models.resource import Resource
from app.models.role import Role
from app.models.user import User
from app.api.utils.auth.password_manager import PasswordManager
from app.api.utils.auth.token_manager import TokenManager
from app.api.utils.config import Config

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlmodel import select
from datetime import timedelta
import jwt


# ---------------------------------------------------
# Config (Load Once)
# ---------------------------------------------------

config = Config()

SECRET_KEY = config.get("SECRET_KEY")
ALGORITHM = config.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(config.get("REFRESH_TOKEN_EXPIRE_MINUTES"))


# ---------------------------------------------------
# Managers
# ---------------------------------------------------

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

token_manager = TokenManager(
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES
)

password_manager = PasswordManager()


# ---------------------------------------------------
# Generic Database Handler Dependency
# ---------------------------------------------------

ModelType = TypeVar("ModelType")

def get_handler(model: Type[ModelType]):
    def _handler(session: Session = Depends(get_session)) -> DatabaseHandler[ModelType]:
        return DatabaseHandler(session, model)
    return _handler


user_auth_handler = get_handler(UserAuth)
user_details_handler = get_handler(UserDetails)
user_handler = get_handler(User)
token_handler = get_handler(Token)
resource_handler = get_handler(Resource)
role_handler = get_handler(Role)


# ---------------------------------------------------
# Authentication Helpers
# ---------------------------------------------------

def hash_password(password: str) -> str:
    return password_manager.hash_password(password)


def authenticate_user(
    username: str,
    password: str,
    db: DatabaseHandler[UserAuth]
) -> UserAuth | None:

    user = db.session.exec(
        select(UserAuth).where(UserAuth.username == username)
    ).first()

    if not user:
        return None

    if not password_manager.verify_password(password, user.password_hash):
        return None

    return user


async def get_user_by_username(
    username: str,
    db: DatabaseHandler[User]
) -> User | None:

    return db.session.exec(
        select(User).where(User.username == username)
    ).first()


async def get_user_details(user: User) -> UserDetails:
    db = DatabaseHandler(next_session, UserDetails)

    return db.session.exec(
        select(UserDetails).where(UserDetails.user.name == user.name)
    ).first()



async def create_access_token(username: str, user_id: int) -> str:
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return token_manager.create_access_token(username, user_id, expires)


# ---------------------------------------------------
# Current User Dependency
# ---------------------------------------------------

async def get_current_user(token: str):

    try:
        payload = token_manager.verify_token(token)

        username = payload.get("sub")
        user_id = payload.get("id")

        if not username or not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
            )

        return {"username": username, "id": user_id}

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


