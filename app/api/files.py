from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import Optional, List
import structlog
import uuid
from app.api.models.requests import FileUploadMetadata, FileQueryParams, FileResponse
from app.api.dependencies import get_file_service, get_current_user
from app.api.services.file_service import FileService
from app.infrastructure.metrics import track_request_metrics

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.post(
    "/upload",
    response_model=FileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload SPL File",
    description="Upload an SPL policy file"
)
@track_request_metrics("file_upload")
async def upload_file(
        file: UploadFile = File(...),
        metadata: Optional[FileUploadMetadata] = None,
        background_tasks: BackgroundTasks = BackgroundTasks(),
        file_service: FileService = Depends(get_file_service),
        current_user: Optional[str] = Depends(get_current_user)
):
    """
    Upload an SPL policy file.

    Supports:
    - .spl files (SPL source code)
    - .json files (policy metadata)
    - .yaml files (policy configuration)

    The file is stored and optionally compiled if auto_compile is enabled.
    """
    logger.info(
        "file_upload_requested",
        filename=file.filename,
        content_type=file.content_type,
        user=current_user
    )

    try:
        # Validate file
        if file.size > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File too large (max 10MB)"
            )

        allowed_types = ["text/plain", "application/json", "application/yaml", "application/x-yaml"]
        allowed_extensions = [".spl", ".json", ".yaml", ".yml"]

        file_ext = "." + file.filename.split(".")[-1] if "." in file.filename else ""
        if file_ext.lower() not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )

        # Read file content
        content = await file.read()

        # Create file record
        file_id = str(uuid.uuid4())
        file_metadata = metadata or FileUploadMetadata(
            filename=file.filename,
            content_type=file.content_type or "text/plain"
        )

        # Store file
        file_response = await file_service.store_file(
            file_id=file_id,
            filename=file.filename,
            content=content,
            metadata=file_metadata,
            uploaded_by=current_user
        )

        logger.info(
            "file_uploaded",
            file_id=file_id,
            filename=file.filename,
            size=len(content)
        )

        # Auto-compile if requested
        if file_metadata.auto_compile and file_ext == ".spl":
            background_tasks.add_task(
                file_service.compile_file,
                file_id,
                content.decode('utf-8')
            )
            logger.info("auto_compile_scheduled", file_id=file_id)

        return file_response

    except HTTPException:
        raise
    except Exception as e:
        logger.error("file_upload_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File upload failed: {str(e)}"
        )


@router.get(
    "/{file_id}",
    response_model=FileResponse,
    summary="Get File Metadata",
    description="Get metadata for an uploaded file"
)
@track_request_metrics("get_file_metadata")
async def get_file_metadata(
        file_id: str,
        file_service: FileService = Depends(get_file_service),
        current_user: Optional[str] = Depends(get_current_user)
):
    """Get file metadata by ID."""
    try:
        file_metadata = await file_service.get_file_metadata(file_id)

        if not file_metadata:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File {file_id} not found"
            )

        return file_metadata

    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_file_metadata_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve file metadata"
        )


@router.get(
    "/{file_id}/download",
    summary="Download File",
    description="Download file content"
)
@track_request_metrics("download_file")
async def download_file(
        file_id: str,
        file_service: FileService = Depends(get_file_service),
        current_user: Optional[str] = Depends(get_current_user)
):
    """Download file content."""
    try:
        file_data = await file_service.get_file_content(file_id)

        if not file_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File {file_id} not found"
            )

        logger.info(
            "file_downloaded",
            file_id=file_id,
            user=current_user
        )

        return StreamingResponse(
            iter([file_data["content"]]),
            media_type=file_data["content_type"],
            headers={
                "Content-Disposition": f'attachment; filename="{file_data["filename"]}"'
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("download_file_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to download file"
        )


@router.delete(
    "/{file_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete File",
    description="Delete an uploaded file"
)
@track_request_metrics("delete_file")
async def delete_file(
        file_id: str,
        file_service: FileService = Depends(get_file_service),
        current_user: Optional[str] = Depends(get_current_user)
):
    """Delete file by ID."""
    try:
        success = await file_service.delete_file(file_id, user=current_user)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File {file_id} not found"
            )

        logger.info("file_deleted", file_id=file_id, user=current_user)

    except HTTPException:
        raise
    except Exception as e:
        logger.error("delete_file_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete file"
        )


@router.get(
    "/",
    response_model=List[FileResponse],
    summary="List Files",
    description="List uploaded files with pagination and filtering"
)
@track_request_metrics("list_files")
async def list_files(
        skip: int = 0,
        limit: int = 20,
        tags: Optional[str] = None,
        search: Optional[str] = None,
        file_service: FileService = Depends(get_file_service),
        current_user: Optional[str] = Depends(get_current_user)
):
    """
    List files with optional filtering.

    Query parameters:
    - skip: Number of records to skip (pagination)
    - limit: Maximum records to return (1-100)
    - tags: Comma-separated list of tags to filter by
    - search: Search query for filename or description
    """
    try:
        tag_list = tags.split(",") if tags else None

        files = await file_service.list_files(
            skip=skip,
            limit=min(limit, 100),
            tags=tag_list,
            search=search,
            user=current_user
        )

        return files

    except Exception as e:
        logger.error("list_files_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list files"
        )


@router.post(
    "/{file_id}/compile",
    response_model=Dict[str, Any],
    summary="Compile File",
    description="Compile an uploaded SPL file"
)
@track_request_metrics("compile_file")
async def compile_file(
        file_id: str,
        background_tasks: BackgroundTasks,
        file_service: FileService = Depends(get_file_service),
        current_user: Optional[str] = Depends(get_current_user)
):
    """Compile an uploaded file."""
    try:
        # Get file content
        file_data = await file_service.get_file_content(file_id)

        if not file_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File {file_id} not found"
            )

        # Check if file is SPL
        if not file_data["filename"].endswith(".spl"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .spl files can be compiled"
            )

        # Compile in background
        background_tasks.add_task(
            file_service.compile_file,
            file_id,
            file_data["content"].decode('utf-8')
        )

        return {
            "status": "compiling",
            "file_id": file_id,
            "message": "Compilation started in background"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("compile_file_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to compile file"
        )