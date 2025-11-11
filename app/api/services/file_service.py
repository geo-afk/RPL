
from api.models.responses import FileResponse
from infrastructure.storage import FileStorage


class FileService:
    """Service for file operations."""

    def __init__(self, database=None, storage: Optional[FileStorage] = None):
        self.db = database
        self.storage = storage or FileStorage()
        logger.info("file_service_initialized")

    async def store_file(
            self,
            file_id: str,
            filename: str,
            content: bytes,
            metadata,
            uploaded_by: Optional[str] = None
    ) -> FileResponse:
        """Store a file."""
        logger.info(
            "storing_file",
            file_id=file_id,
            filename=filename,
            size=len(content)
        )

        # Save file content
        storage_path = await self.storage.save(file_id, content)

        # Store metadata in database
        file_data = {
            "id": file_id,
            "filename": filename,
            "size": len(content),
            "content_type": metadata.content_type,
            "description": metadata.description,
            "tags": metadata.tags or [],
            "storage_path": storage_path,
            "uploaded_at": datetime.utcnow(),
            "uploaded_by": uploaded_by
        }

        if self.db:
            from infrastructure.database import FileModel, get_session
            async with get_session() as session:
                file_model = FileModel(**file_data)
                session.add(file_model)
                await session.commit()

        logger.info("file_stored", file_id=file_id)

        return FileResponse(
            id=file_id,
            filename=filename,
            size=len(content),
            content_type=metadata.content_type,
            description=metadata.description,
            tags=metadata.tags or [],
            uploaded_at=datetime.utcnow(),
            uploaded_by=uploaded_by,
            download_url=f"/api/v1/files/{file_id}/download"
        )

    async def get_file_metadata(self, file_id: str) -> Optional[FileResponse]:
        """Get file metadata."""
        if not self.db:
            return None

        from infrastructure.database import FileModel, get_session
        async with get_session() as session:
            file_model = await session.get(FileModel, file_id)
            if file_model:
                return FileResponse(
                    id=file_model.id,
                    filename=file_model.filename,
                    size=file_model.size,
                    content_type=file_model.content_type,
                    description=file_model.description,
                    tags=file_model.tags or [],
                    uploaded_at=file_model.uploaded_at,
                    uploaded_by=file_model.uploaded_by,
                    processed=file_model.processed,
                    policy_id=file_model.policy_id,
                    download_url=f"/api/v1/files/{file_id}/download"
                )

        return None

    async def get_file_content(self, file_id: str) -> Optional[Dict[str, Any]]:
        """Get file content."""
        # Get metadata
        metadata = await self.get_file_metadata(file_id)
        if not metadata:
            return None

        # Get content from storage
        content = await self.storage.read(file_id)
        if not content:
            return None

        return {
            "filename": metadata.filename,
            "content": content,
            "content_type": metadata.content_type
        }

    async def delete_file(self, file_id: str, user: Optional[str] = None) -> bool:
        """Delete a file."""
        logger.info("deleting_file", file_id=file_id, user=user)

        # Delete from storage
        await self.storage.delete(file_id)

        # Delete from database
        if self.db:
            from infrastructure.database import FileModel, get_session
            async with get_session() as session:
                file_model = await session.get(FileModel, file_id)
                if file_model:
                    await session.delete(file_model)
                    await session.commit()
                    logger.info("file_deleted", file_id=file_id)
                    return True

        return False

    async def list_files(
            self,
            skip: int = 0,
            limit: int = 20,
            tags: Optional[List[str]] = None,
            search: Optional[str] = None,
            user: Optional[str] = None
    ) -> List[FileResponse]:
        """List files."""
        if not self.db:
            return []

        from infrastructure.database import FileModel, get_session
        from sqlalchemy import select

        async with get_session() as session:
            query = select(FileModel).offset(skip).limit(limit)
            result = await session.execute(query)
            files = result.scalars().all()

            return [
                FileResponse(
                    id=f.id,
                    filename=f.filename,
                    size=f.size,
                    content_type=f.content_type,
                    description=f.description,
                    tags=f.tags or [],
                    uploaded_at=f.uploaded_at,
                    uploaded_by=f.uploaded_by,
                    processed=f.processed,
                    policy_id=f.policy_id,
                    download_url=f"/api/v1/files/{f.id}/download"
                )
                for f in files
            ]

    async def compile_file(self, file_id: str, code: str):
        """Compile a file (background task)."""
        logger.info("compiling_file", file_id=file_id)

        # This would call the compiler service
        # For now, just mark as processed
        if self.db:
            from infrastructure.database import FileModel, get_session
            async with get_session() as session:
                file_model = await session.get(FileModel, file_id)
                if file_model:
                    file_model.processed = True
                    await session.commit()

