from sqlmodel import Session
from app.api.database.database import engine
from typing import Generator

def get_client_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
