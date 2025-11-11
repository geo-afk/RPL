
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import List, Dict, Any
import structlog
import time

from app.api.models.requests import (
    EnforcementRequest,
    BatchEnforcementRequest,
    EnforcementResult
)
from api.dependencies import get_enforcement_service, get_current_user
from api.services.enforcement_service import EnforcementService
from infrastructure.metrics import track_request_metrics
from infrastructure.cache import get_cache

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.post(
    "/check",
    response_model=EnforcementResult,
    summary="Check Policy Enforcement",
    description="Check if an action is allowed by policy"
)
@track_request_metrics("enforcement_check")
async def check_enforcement(
        request: EnforcementRequest,
        background_tasks: BackgroundTasks,
        enforcement_service: EnforcementService = Depends(get_enforcement_service),
        current_user: Optional[str] = Depends(get_current_user),
        cache=Depends(get_cache)
):
    """
    Check if a subject is allowed to perform an action on a resource.

    This is the policies policy enforcement endpoint used for:
    - Access control decisions
    - Real-time authorization
    - Audit logging

    Returns:
    - allowed: Boolean indicating if access is granted
    - matched_rules: List of policy rules that matched
    - reason: Explanation for the decision
    - evaluation_time_ms: Time taken to evaluate
    """
    start_time = time.time()

    logger.info(
        "enforcement_check_requested",
        policy_id=request.policy_id,
        subject=request.subject,
        action=request.action,
        resource=request.resource,
        user=current_user
    )

    try:
        # Check cache for recent identical request
        cache_key = (
            f"enforce:{request.policy_id}:{request.subject}:"
            f"{request.action}:{request.resource}"
        )

        if cache:
            cached_result = await cache.get(cache_key)
            if cached_result:
                logger.debug("enforcement_cache_hit", cache_key=cache_key)
                return EnforcementResult(**cached_result)

        # Evaluate policy
        result = await enforcement_service.check_access(
            policy_id=request.policy_id,
            subject=request.subject,
            action=request.action,
            resource=request.resource,
            context=request.context or {}
        )

        # Calculate evaluation time
        evaluation_time = (time.time() - start_time) * 1000
        result.evaluation_time_ms = evaluation_time

        logger.info(
            "enforcement_check_completed",
            policy_id=request.policy_id,
            subject=request.subject,
            action=request.action,
            resource=request.resource,
            allowed=result.allowed,
            evaluation_time_ms=evaluation_time
        )

        # Cache result (short TTL for security)
        if cache:
            background_tasks.add_task(
                cache.set,
                cache_key,
                result.dict(),
                expire=60  # 1 minute cache
            )

        # Log enforcement decision asynchronously
        background_tasks.add_task(
            enforcement_service.log_enforcement,
            result
        )

        return result

    except ValueError as e:
        logger.warning("enforcement_check_validation_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Validation Error", "message": str(e)}
        )

    except Exception as e:
        logger.error("enforcement_check_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Enforcement Check Failed", "message": str(e)}
        )


@router.post(
    "/batch-check",
    response_model=List[EnforcementResult],
    summary="Batch Check Policy Enforcement",
    description="Check multiple enforcement decisions in one request"
)
@track_request_metrics("batch_enforcement_check")
async def batch_check_enforcement(
        request: BatchEnforcementRequest,
        background_tasks: BackgroundTasks,
        enforcement_service: EnforcementService = Depends(get_enforcement_service),
        current_user: Optional[str] = Depends(get_current_user)
):
    """
    Check multiple enforcement decisions efficiently.

    Useful for:
    - Bulk permission checks
    - Pre-loading permissions for UI
    - Optimizing multi-resource access checks

    Limitations:
    - Maximum 100 requests per batch
    """
    if len(request.requests) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 100 requests per batch"
        )

    logger.info(
        "batch_enforcement_check_requested",
        policy_id=request.policy_id,
        count=len(request.requests),
        user=current_user
    )

    try:
        start_time = time.time()

        # Process all requests
        results = await enforcement_service.batch_check_access(
            policy_id=request.policy_id,
            requests=request.requests
        )

        total_time = (time.time() - start_time) * 1000
        avg_time = total_time / len(results) if results else 0

        logger.info(
            "batch_enforcement_check_completed",
            policy_id=request.policy_id,
            count=len(results),
            allowed=sum(1 for r in results if r.allowed),
            denied=sum(1 for r in results if not r.allowed),
            total_time_ms=total_time,
            avg_time_ms=avg_time
        )

        # Log all enforcement decisions
        background_tasks.add_task(
            enforcement_service.batch_log_enforcement,
            results
        )

        return results

    except Exception as e:
        logger.error("batch_enforcement_check_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Batch Enforcement Check Failed", "message": str(e)}
        )


@router.get(
    "/history/{policy_id}",
    response_model=List[EnforcementResult],
    summary="Get Enforcement History",
    description="Get enforcement decision history for a policy"
)
@track_request_metrics("get_enforcement_history")
async def get_enforcement_history(
        policy_id: str,
        limit: int = 100,
        subject: Optional[str] = None,
        resource: Optional[str] = None,
        enforcement_service: EnforcementService = Depends(get_enforcement_service),
        current_user: Optional[str] = Depends(get_current_user)
):
    """
    Get enforcement decision history.

    Useful for:
    - Auditing access decisions
    - Analyzing access patterns
    - Debugging policy issues

    Query parameters:
    - limit: Maximum number of records (1-1000)
    - subject: Filter by subject/user
    - resource: Filter by resource
    """
    try:
        history = await enforcement_service.get_enforcement_history(
            policy_id=policy_id,
            limit=min(limit, 1000),
            subject=subject,
            resource=resource
        )

        logger.info(
            "enforcement_history_retrieved",
            policy_id=policy_id,
            count=len(history)
        )

        return history

    except Exception as e:
        logger.error("get_enforcement_history_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve enforcement history"
        )


@router.get(
    "/stats/{policy_id}",
    response_model=Dict[str, Any],
    summary="Get Enforcement Statistics",
    description="Get statistics about policy enforcement"
)
@track_request_metrics("get_enforcement_stats")
async def get_enforcement_stats(
        policy_id: str,
        enforcement_service: EnforcementService = Depends(get_enforcement_service),
        current_user: Optional[str] = Depends(get_current_user)
):
    """
    Get enforcement statistics for a policy.

    Returns:
    - Total enforcement checks
    - Allow/deny ratio
    - Most accessed resources
    - Most active subjects
    - Average evaluation time
    """
    try:
        stats = await enforcement_service.get_enforcement_stats(policy_id)

        logger.info(
            "enforcement_stats_retrieved",
            policy_id=policy_id
        )

        return stats

    except Exception as e:
        logger.error("get_enforcement_stats_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve enforcement statistics"
        )


@router.post(
    "/simulate",
    response_model=EnforcementResult,
    summary="Simulate Policy Enforcement",
    description="Simulate enforcement without logging (for testing)"
)
@track_request_metrics("simulate_enforcement")
async def simulate_enforcement(
        request: EnforcementRequest,
        enforcement_service: EnforcementService = Depends(get_enforcement_service),
        current_user: Optional[str] = Depends(get_current_user)
):
    """
    Simulate policy enforcement without logging the decision.

    Useful for:
    - Testing policies before deployment
    - "What-if" analysis
    - Policy development

    Note: This does not log the decision or affect audit trails.
    """
    logger.info(
        "enforcement_simulation_requested",
        policy_id=request.policy_id,
        subject=request.subject,
        action=request.action,
        resource=request.resource
    )

    try:
        result = await enforcement_service.check_access(
            policy_id=request.policy_id,
            subject=request.subject,
            action=request.action,
            resource=request.resource,
            context=request.context or {},
            simulate=True  # Don't log
        )

        logger.info(
            "enforcement_simulation_completed",
            policy_id=request.policy_id,
            allowed=result.allowed
        )

        return result

    except Exception as e:
        logger.error("enforcement_simulation_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Simulation failed"
        )


@router.post(
    "/explain",
    response_model=Dict[str, Any],
    summary="Explain Enforcement Decision",
    description="Get detailed explanation of why a decision was made"
)
@track_request_metrics("explain_enforcement")
async def explain_enforcement(
        request: EnforcementRequest,
        enforcement_service: EnforcementService = Depends(get_enforcement_service),
        current_user: Optional[str] = Depends(get_current_user)
):
    """
    Get detailed explanation of enforcement decision.

    Returns:
    - Decision (allow/deny)
    - All evaluated rules
    - Rule evaluation results
    - Step-by-step explanation
    - Suggested policy changes (if denied)

    Useful for:
    - Debugging policy issues
    - Understanding complex policies
    - Training and documentation
    """
    try:
        explanation = await enforcement_service.explain_decision(
            policy_id=request.policy_id,
            subject=request.subject,
            action=request.action,
            resource=request.resource,
            context=request.context or {}
        )

        logger.info(
            "enforcement_explanation_generated",
            policy_id=request.policy_id,
            subject=request.subject
        )

        return explanation

    except Exception as e:
        logger.error("explain_enforcement_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate explanation"
        )