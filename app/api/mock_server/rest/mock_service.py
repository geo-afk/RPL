from sqlmodel import Session
from app.api.database.database import engine
from typing import Generator, Any


def get_db() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session
