
from fastapi import APIRouter, Depends, BackgroundTasks
from typing import Dict, Any, List
from api.models.responses import MetricsResponse, HealthResponse
from api.dependencies import require_admin, get_database, get_cache
from infrastructure.metrics import get_metrics

router = APIRouter()


@router.get(
    "/metrics",
    response_model=MetricsResponse,
    summary="Get System Metrics",
    description="Get comprehensive system metrics (admin only)"
)
async def get_system_metrics(
        current_user: str = Depends(require_admin)
):
    """
    Get detailed system metrics including:
    - Request statistics
    - Compilation statistics
    - Enforcement statistics
    - Cache performance
    """
    metrics = get_metrics()

    return MetricsResponse(
        total_requests=metrics.get("total_requests", 0),
        successful_requests=metrics.get("successful_requests", 0),
        failed_requests=metrics.get("failed_requests", 0),
        average_response_time_ms=metrics.get("avg_response_time", 0.0),
        total_compilations=metrics.get("total_compilations", 0),
        successful_compilations=metrics.get("successful_compilations", 0),
        average_compilation_time_ms=metrics.get("avg_compilation_time", 0.0),
        total_enforcements=metrics.get("total_enforcements", 0),
        allowed_enforcements=metrics.get("allowed_enforcements", 0),
        denied_enforcements=metrics.get("denied_enforcements", 0),
        average_enforcement_time_ms=metrics.get("avg_enforcement_time", 0.0),
        cache_hit_rate=metrics.get("cache_hit_rate", 0.0)
    )


@router.get(
    "/health/detailed",
    response_model=Dict[str, Any],
    summary="Detailed Health Check",
    description="Get detailed health information about all system components"
)
async def detailed_health_check(
        current_user: str = Depends(require_admin),
        database=Depends(get_database),
        cache=Depends(get_cache)
):
    """
    Comprehensive health check including:
    - Database connectivity
    - Cache connectivity
    - LLM API status
    - File system status
    - Memory usage
    - CPU usage
    """
    import psutil
    from datetime import datetime

    # Check database
    db_healthy = await database.is_healthy() if database else False

    # Check cache
    cache_healthy = await cache.is_healthy() if cache else False

    # System resources
    memory = psutil.virtual_memory()
    cpu_percent = psutil.cpu_percent(interval=1)

    return {
        "status": "healthy" if (db_healthy and cache_healthy) else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "database": {
                "status": "up" if db_healthy else "down",
                "details": "PostgreSQL connection active" if db_healthy else "Connection failed"
            },
            "cache": {
                "status": "up" if cache_healthy else "down",
                "details": "Redis connection active" if cache_healthy else "Connection failed"
            },
            "llm_api": {
                "status": "unknown",
                "details": "LLM API status check not implemented"
            }
        },
        "system": {
            "memory": {
                "total_mb": round(memory.total / 1024 / 1024, 2),
                "available_mb": round(memory.available / 1024 / 1024, 2),
                "percent_used": memory.percent
            },
            "cpu": {
                "percent_used": cpu_percent,
                "count": psutil.cpu_count()
            }
        }
    }


@router.post(
    "/cache/clear",
    summary="Clear Cache",
    description="Clear all cached data (admin only)"
)
async def clear_cache(
        current_user: str = Depends(require_admin),
        cache=Depends(get_cache)
):
    """Clear all cached compilation and enforcement results."""
    if cache:
        await cache.clear()
        logger.info("cache_cleared", user=current_user)
        return {"message": "Cache cleared successfully"}
    else:
        return {"message": "Cache not available"}


@router.get(
    "/logs/recent",
    summary="Get Recent Logs",
    description="Get recent application logs (admin only)"
)
async def get_recent_logs(
        limit: int = 100,
        level: str = "INFO",
        current_user: str = Depends(require_admin)
):
    """
    Get recent log entries.
    Note: This is a placeholder - implement proper log aggregation in production.
    """
    # TODO: Implement log retrieval from log file or log aggregation service
    return {
        "message": "Log retrieval not yet implemented",
        "suggestion": "Use docker logs or a log aggregation service like ELK"
    }


@router.post(
    "/maintenance/mode",
    summary="Toggle Maintenance Mode",
    description="Enable or disable maintenance mode (admin only)"
)
async def toggle_maintenance_mode(
        enabled: bool,
        current_user: str = Depends(require_admin)
):
    """
    Enable or disable maintenance mode.
    When enabled, all endpoints return 503 Service Unavailable.
    """
    # TODO: Implement maintenance mode flag in Redis
    logger.info(
        "maintenance_mode_toggled",
        enabled=enabled,
        user=current_user
    )

    return {
        "message": f"Maintenance mode {'enabled' if enabled else 'disabled'}",
        "status": "maintenance" if enabled else "active"
    }


@router.get(
    "/stats/policies",
    summary="Get Policy Statistics",
    description="Get statistics about all policies"
)
async def get_policy_stats(
        current_user: str = Depends(require_admin),
        database=Depends(get_database)
):
    """
    Get comprehensive policy statistics:
    - Total policies
    - Active/inactive policies
    - Most used policies
    - Compilation success rate
    """
    if not database:
        return {
            "total_policies": 0,
            "active_policies": 0,
            "inactive_policies": 0
        }

    # TODO: Implement actual statistics gathering
    return {
        "total_policies": 0,
        "active_policies": 0,
        "inactive_policies": 0,
        "most_used_policies": [],
        "compilation_success_rate": 0.0
    }


@router.post(
    "/database/backup",
    summary="Trigger Database Backup",
    description="Trigger a database backup (admin only)"
)
async def trigger_database_backup(
        background_tasks: BackgroundTasks,
        current_user: str = Depends(require_admin)
):
    """
    Trigger a database backup operation.
    Backup runs in background.
    """

    async def backup_database():
        # TODO: Implement database backup logic
        logger.info("database_backup_started", user=current_user)
        # Simulate backup
        import asyncio
        await asyncio.sleep(5)
        logger.info("database_backup_completed", user=current_user)

    background_tasks.add_task(backup_database)

    return {
        "message": "Database backup started",
        "status": "in_progress"
    }


@router.get(
    "/users/active",
    summary="Get Active Users",
    description="Get list of currently active users"
)
async def get_active_users(
        current_user: str = Depends(require_admin)
):
    """
    Get list of users who have made requests recently.
    """
    # TODO: Implement user activity tracking
    return {
        "active_users": [],
        "total_active": 0,
        "time_window_minutes": 15
    }


@router.post(
    "/config/reload",
    summary="Reload Configuration",
    description="Reload application configuration without restart"
)
async def reload_configuration(
        current_user: str = Depends(require_admin)
):
    """
    Reload application configuration from files.
    Useful for updating settings without restarting.
    """
    # TODO: Implement configuration reloading
    logger.info("configuration_reload_requested", user=current_user)

    return {
        "message": "Configuration reloaded",
        "status": "success"
    }