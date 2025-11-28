from typing import Any, Generator, Generic, Optional, Sequence, Type, TypeVar, Iterable
from sqlmodel import Session, SQLModel, create_engine, select
from app.api.utils.config import Config
import structlog


logger = structlog.get_logger(__name__)
DATABASE_URL = Config().get("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

async def init_db():
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        logger.info("database_session_created")
        yield session


# ------------------------
# Generic CRUD Handler
# ------------------------
T = TypeVar("T", bound=SQLModel)

class DatabaseHandler(Generic[T]):
    def __init__(self, session: Session, model: Type[T]) -> None:
        self.session = session
        self.model = model

    # CREATE ONE
    def create(self, obj_data: T) -> T:
        self.session.add(obj_data)
        self.session.commit()
        self.session.refresh(obj_data)
        return obj_data

    # CREATE MANY
    def create_all(self, objects: Iterable[T]) -> list[T]:
        objs = list(objects)  # convert iterable → list

        if not objs:
            return []

        self.session.add_all(objs)
        self.session.commit()

        for obj in objs:
            self.session.refresh(obj)

        return objs

    # READ (Single)
    def get(self, obj_id: Any) -> Optional[T]:
        return self.session.get(self.model, obj_id)

    # READ (All)
    def get_all(self) -> Sequence[T]:
        statement = select(self.model)
        results = self.session.exec(statement)
        return results.all()

    # UPDATE
    def update(self, obj_id: Any, new_data: dict) -> Optional[T]:
        obj = self.session.get(self.model, obj_id)
        if not obj:
            return None
        for key, value in new_data.items():
            setattr(obj, key, value)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    # DELETE
    def delete(self, obj_id: Any) -> bool:
        obj = self.session.get(self.model, obj_id)
        if not obj:
            return False
        self.session.delete(obj)
        self.session.commit()
        return True

next_session = next(get_session())



