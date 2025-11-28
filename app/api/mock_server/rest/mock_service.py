from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from app.api.database.database import engine

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session

