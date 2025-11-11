import asyncio
import json
import structlog
from typing import Optional, Any
from datetime import datetime, timedelta

logger = structlog.get_logger(__name__)

# Global in-memory store
_memory_store: dict[str, tuple[Any, Optional[datetime]]] = {}
_lock = asyncio.Lock()


async def init_cache():
    """Initialize in-memory cache."""
    global _memory_store
    _memory_store = {}
    logger.info("in_memory_cache_initialized")


async def close_cache():
    """Clear in-memory cache."""
    global _memory_store
    _memory_store.clear()
    logger.info("in_memory_cache_closed")


async def check_cache_health() -> bool:
    """Check in-memory cache health."""
    try:
        _ = len(_memory_store)
        return True
    except Exception as e:
        logger.error("cache_health_check_failed", error=str(e))
        return False


class Cache:
    """In-memory cache wrapper with serialization and optional expiry."""

    def __init__(self):
        self.store = _memory_store
        self.lock = _lock

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        async with self.lock:
            try:
                if key not in self.store:
                    return None

                value, expires_at = self.store[key]
                if expires_at and datetime.now() > expires_at:
                    # Expired — delete and return None
                    del self.store[key]
                    return None

                return json.loads(value)
            except Exception as e:
                logger.error("cache_get_failed", key=key, error=str(e))
                return None

    async def set(self, key: str, value: Any, expire: Optional[int] = None):
        """Set value in cache with optional expiry (seconds)."""
        async with self.lock:
            try:
                serialized = json.dumps(value)
                expires_at = (
                    datetime.now() + timedelta(seconds=expire)
                    if expire
                    else None
                )
                self.store[key] = (serialized, expires_at)
            except Exception as e:
                logger.error("cache_set_failed", key=key, error=str(e))

    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        async with self.lock:
            try:
                if key in self.store:
                    del self.store[key]
                    return True
                return False
            except Exception as e:
                logger.error("cache_delete_failed", key=key, error=str(e))
                return False

    async def clear(self):
        """Clear all cache."""
        async with self.lock:
            try:
                self.store.clear()
                logger.info("cache_cleared")
            except Exception as e:
                logger.error("cache_clear_failed", error=str(e))

    async def is_healthy(self) -> bool:
        """Check if cache is healthy."""
        return await check_cache_health()


def get_cache() -> Optional[Cache]:
    """Get cache instance."""
    return Cache()
