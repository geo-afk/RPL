import aiofiles
from pathlib import Path
from typing import Optional
import structlog

logger = structlog.get_logger(__name__)


class FileStorage:
    """File storage handler (local filesystem)."""

    def __init__(self, base_path: str = "./uploads"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info("file_storage_initialized", path=str(self.base_path))

    async def save(self, file_id: str, content: bytes) -> str:
        """Save file content."""
        file_path = self.base_path / file_id

        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)

        logger.info("file_saved", file_id=file_id, size=len(content))
        return str(file_path)

    async def read(self, file_id: str) -> Optional[bytes]:
        """Read file content."""
        file_path = self.base_path / file_id

        if not file_path.exists():
            logger.warning("file_not_found", file_id=file_id)
            return None

        async with aiofiles.open(file_path, 'rb') as f:
            content = await f.read()

        logger.info("file_read", file_id=file_id, size=len(content))
        return content

    async def delete(self, file_id: str) -> bool:
        """Delete file."""
        file_path = self.base_path / file_id

        if file_path.exists():
            file_path.unlink()
            logger.info("file_deleted", file_id=file_id)
            return True

        return False

    async def exists(self, file_id: str) -> bool:
        """Check if file exists."""
        file_path = self.base_path / file_id
        return file_path.exists()


