from app.api.database.database import Session, DatabaseHandler, get_session
from app.api.utils.auth.password_manager import PasswordManager
from app.api.utils.auth.token_manager import TokenManager
from app.models.auth_models import UserAuth, Token
from fastapi.security import OAuth2PasswordBearer
from app.api.utils.config import Config
from datetime import timedelta
from typing import Annotated
from sqlmodel import select
from fastapi import Depends
import jwt



SECRET_KEY = Config().get("SECRET_KEY")
ALGORITHM = Config().get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(Config().get("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(Config().get("REFRESH_TOKEN_EXPIRE_MINUTES"))


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
token_manager = TokenManager(
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES
)
password_manager = PasswordManager()


def user_auth_handler(session: Session = Depends(get_session)) -> DatabaseHandler[UserAuth]:
    return DatabaseHandler(session, UserAuth)


def token_handler(session: Session = Depends(get_session)) -> DatabaseHandler[Token]:
    return DatabaseHandler(session, Token)


def authenticate_user(username: str, password: str, db: DatabaseHandler) -> UserAuth | None:
    statement = select(UserAuth).where(UserAuth.username == username)
    user = db.session.exec(statement).first()

    if not user:
        return None
    if not password_manager.verify_password(password, user.password_hash):
        return None
    return user





def create_access_token(username: str, user_id: int) -> str:
    expires_delta = timedelta(minutes=token_manager.access_token_expire)
    encoded_jwt = token_manager.create_access_token(username, user_id, expires_delta)

    return encoded_jwt



async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = token_manager.verify_token(token)

        if not payload:
            return None

        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        
        if username is None or user_id is None:
            return None
        return {"username": username, "id": user_id}
    except jwt.PyJWTError:
        return None


user_dependency = Annotated[dict, Depends(get_current_user)]