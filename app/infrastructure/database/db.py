from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine
from app.infrastructure.database.models import PolicyModel
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import declarative_base
from datetime import datetime, UTC
import structlog

logger = structlog.get_logger(__name__)


Base = declarative_base()


# Database connection
_engine: Optional[AsyncEngine] = None
_session_maker: Optional[async_sessionmaker] = None


async def init_db(database_url: str = None):
    """Initialize database connection."""
    global _engine, _session_maker

    if database_url is None:
        import os
        database_url = os.getenv(
            "DATABASE_URL",
            "postgresql+asyncpg://spl_user:spl_password@localhost:5432/spl_db"
        )

    logger.info("initializing_database", url=database_url.split("@")[0])

    _engine = create_async_engine(
        database_url,
        echo=False,
        pool_size=10,
        max_overflow=20
    )

    _session_maker = async_sessionmaker(
        _engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    # Create tables
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("database_initialized")


async def close_db():
    """Close database connection."""
    global _engine
    if _engine:
        await _engine.dispose()
        logger.info("database_closed")


async def check_db_health() -> bool:
    """Check database health."""
    try:
        async with _session_maker() as session:
            await session.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error("database_health_check_failed", error=str(e))
        return False


def get_session() -> AsyncSession:
    """Get database session."""
    return _session_maker()


# Repository pattern
class PolicyRepository:
    """Repository for policy operations."""

    @staticmethod
    async def create(self, policy_data: Dict[str, Any]) -> PolicyModel:
        """Create a new policy."""
        async with get_session() as session:
            policy = PolicyModel(**policy_data)
            session.add(policy)
            await session.commit()
            await session.refresh(policy)
            return policy

    async def get(self, policy_id: str) -> Optional[PolicyModel]:
        """Get policy by ID."""
        async with get_session() as session:
            result = await session.get(PolicyModel, policy_id)
            return result

    @staticmethod
    async def list(
            self,
            skip: int = 0,
            limit: int = 20,
            **filters
    ) -> List[PolicyModel]:
        """List policies with filters."""
        async with get_session() as session:
            from sqlalchemy import select
            query = select(PolicyModel)

            # Apply filters
            if filters.get("enabled") is not None:
                query = query.where(PolicyModel.enabled == filters["enabled"])

            query = query.offset(skip).limit(limit)
            result = await session.execute(query)
            return list(result.scalars().all())

    @staticmethod
    async def update(self, policy_id: str, updates: Dict[str, Any]) -> Optional[PolicyModel]:
        """Update policy."""
        async with get_session() as session:
            policy = await session.get(PolicyModel, policy_id)
            if policy:
                for key, value in updates.items():
                    setattr(policy, key, value)
                policy.updated_at = lambda: datetime.now(UTC)
                await session.commit()
                await session.refresh(policy)
            return policy

    @staticmethod
    async def delete(self, policy_id: str) -> bool:
        """Delete policy."""
        async with get_session() as session:
            policy = await session.get(PolicyModel, policy_id)
            if policy:
                await session.delete(policy)
                await session.commit()
                return True
            return False

