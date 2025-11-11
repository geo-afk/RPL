from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import List, Optional
import structlog

from app.api.models.requests import (
    PolicyCreateRequest,
    PolicyUpdateRequest
)
from app.api.models.responses import PolicyResponse
from app.api.services.policy_service import PolicyService
from app.api.dependencies import get_policy_service, get_current_user, require_authentication
from app.infrastructure.metrics import track_request_metrics

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.post(
    "/",
    response_model=PolicyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Policy",
    description="Create a new RPL policy"
)
@track_request_metrics("create_policy")
async def create_policy(
        request: PolicyCreateRequest,
        policy_service: PolicyService = Depends(get_policy_service),
        current_user: Optional[str] = Depends(get_current_user)
):
    """
    Create a new policy.

    The policy will be stored but not compiled until explicitly requested.
    """
    logger.info(
        "policy_creation_requested",
        name=request.name,
        user=current_user
    )

    try:
        policy = await policy_service.create_policy(request, user=current_user)

        logger.info(
            "policy_created",
            policy_id=policy.id,
            name=policy.name
        )

        return policy

    except Exception as e:
        logger.error("policy_creation_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create policy: {str(e)}"
        )


@router.get(
    "/{policy_id}",
    response_model=PolicyResponse,
    summary="Get Policy",
    description="Get policy by ID"
)
@track_request_metrics("get_policy")
async def get_policy(
        policy_id: str,
        policy_service: PolicyService = Depends(get_policy_service),
        current_user: Optional[str] = Depends(get_current_user)
):
    """Get a specific policy by ID."""
    policy = await policy_service.get_policy(policy_id)

    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Policy {policy_id} not found"
        )

    return policy


@router.get(
    "/",
    response_model=List[PolicyResponse],
    summary="List Policies",
    description="List all policies with filtering and pagination"
)
@track_request_metrics("list_policies")
async def list_policies(
        skip: int = 0,
        limit: int = 20,
        enabled: Optional[bool] = None,
        tags: Optional[str] = None,
        search: Optional[str] = None,
        policy_service: PolicyService = Depends(get_policy_service),
        current_user: Optional[str] = Depends(get_current_user)
):
    """
    List policies with optional filters.

    Query parameters:
    - skip: Number of records to skip (pagination)
    - limit: Maximum records to return (1-100)
    - enabled: Filter by enabled status
    - tags: Comma-separated list of tags to filter by
    - search: Search query for name or description
    """
    tag_list = tags.split(",") if tags else None

    policies = await policy_service.list_policies(
        skip=skip,
        limit=min(limit, 100),
        enabled=enabled,
        tags=tag_list,
        search=search
    )

    return policies


@router.put(
    "/{policy_id}",
    response_model=PolicyResponse,
    summary="Update Policy",
    description="Update an existing policy"
)
@track_request_metrics("update_policy")
async def update_policy(
        policy_id: str,
        request: PolicyUpdateRequest,
        policy_service: PolicyService = Depends(get_policy_service),
        current_user: Optional[str] = Depends(get_current_user)
):
    """
    Update a policy.

    If code is updated, the policy will need to be recompiled.
    """
    logger.info(
        "policy_update_requested",
        policy_id=policy_id,
        user=current_user
    )

    policy = await policy_service.update_policy(
        policy_id, request, user=current_user
    )

    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Policy {policy_id} not found"
        )

    logger.info("policy_updated", policy_id=policy_id)
    return policy


@router.delete(
    "/{policy_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Policy",
    description="Delete a policy"
)
@track_request_metrics("delete_policy")
async def delete_policy(
        policy_id: str,
        policy_service: PolicyService = Depends(get_policy_service),
        current_user: Optional[str] = Depends(get_current_user)
):
    """Delete a policy permanently."""
    logger.info(
        "policy_deletion_requested",
        policy_id=policy_id,
        user=current_user
    )

    success = await policy_service.delete_policy(policy_id, user=current_user)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Policy {policy_id} not found"
        )

    logger.info("policy_deleted", policy_id=policy_id)


@router.post(
    "/{policy_id}/compile",
    summary="Compile Policy",
    description="Compile a policy"
)
@track_request_metrics("compile_policy")
async def compile_policy(
        policy_id: str,
        background_tasks: BackgroundTasks,
        policy_service: PolicyService = Depends(get_policy_service),
        current_user: Optional[str] = Depends(get_current_user)
):
    """
    Compile a policy.

    Compilation happens in the background.
    Check the policy status to see when it's complete.
    """
    logger.info(
        "policy_compilation_requested",
        policy_id=policy_id,
        user=current_user
    )

    # Get compiler service
    from api.dependencies import get_compiler_service
    compiler_service = get_compiler_service()

    # Compile in background
    background_tasks.add_task(
        policy_service.compile_policy,
        policy_id,
        compiler_service
    )

    return {
        "message": "Policy compilation started",
        "policy_id": policy_id,
        "status": "compiling"
    }


@router.post(
    "/{policy_id}/enable",
    response_model=PolicyResponse,
    summary="Enable Policy",
    description="Enable a policy for enforcement"
)
@track_request_metrics("enable_policy")
async def enable_policy(
        policy_id: str,
        policy_service: PolicyService = Depends(get_policy_service),
        current_user: Optional[str] = Depends(get_current_user)
):
    """Enable a policy."""
    from api.models.requests import PolicyUpdateRequest

    policy = await policy_service.update_policy(
        policy_id,
        PolicyUpdateRequest(enabled=True),
        user=current_user
    )

    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Policy {policy_id} not found"
        )

    logger.info("policy_enabled", policy_id=policy_id, user=current_user)
    return policy


@router.post(
    "/{policy_id}/disable",
    response_model=PolicyResponse,
    summary="Disable Policy",
    description="Disable a policy"
)
@track_request_metrics("disable_policy")
async def disable_policy(
        policy_id: str,
        policy_service: PolicyService = Depends(get_policy_service),
        current_user: Optional[str] = Depends(get_current_user)
):
    """Disable a policy."""
    from api.models.requests import PolicyUpdateRequest

    policy = await policy_service.update_policy(
        policy_id,
        PolicyUpdateRequest(enabled=False),
        user=current_user
    )

    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Policy {policy_id} not found"
        )

    logger.info("policy_disabled", policy_id=policy_id, user=current_user)
    return policy

