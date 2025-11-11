"""
FastAPI Application Entry Point
api/main.py
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import time
import structlog

from api.routers import compiler, policies, files, enforcement, admin
from api.middleware import LoggingMiddleware, RateLimitMiddleware
from infrastructure.database import init_db, close_db
from infrastructure.cache import init_cache, close_cache
from infrastructure.metrics import metrics_middleware, PrometheusMetrics
from infrastructure.logging_config import setup_logging

# Setup structured logging
setup_logging()
logger = structlog.get_logger(__name__)

# Initialize metrics
prometheus_metrics = PrometheusMetrics()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for startup and shutdown events.
    Handles database connections, cache, and other resources.
    """
    # Startup
    logger.info("application_starting", version=app.version)

    try:
        # Initialize database
        await init_db()
        logger.info("database_initialized")

        # Initialize cache
        await init_cache()
        logger.info("cache_initialized")

        # Initialize metrics
        prometheus_metrics.setup()
        logger.info("metrics_initialized")

        logger.info("application_ready")

        yield  # Application is running

    finally:
        # Shutdown
        logger.info("application_shutting_down")

        # Close connections
        await close_cache()
        logger.info("cache_closed")

        await close_db()
        logger.info("database_closed")

        logger.info("application_shutdown_complete")


# Create FastAPI application
app = FastAPI(
    title="RPL Compiler API",
    description="Secure Policy Language Compiler with REST API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# ============================================================
# MIDDLEWARE CONFIGURATION
# ============================================================

# CORS - Allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on environment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gzip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Metrics collection
app.middleware("http")(metrics_middleware)

# Custom logging
app.add_middleware(LoggingMiddleware)

# Rate limiting
app.add_middleware(RateLimitMiddleware)


# ============================================================
# EXCEPTION HANDLERS
# ============================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
):
    """Handle validation errors with detailed messages."""
    logger.warning(
        "validation_error",
        path=request.url.path,
        errors=exc.errors()
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "details": exc.errors(),
            "body": exc.body
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors gracefully."""
    logger.error(
        "unexpected_error",
        path=request.url.path,
        error=str(exc),
        exc_info=True
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred"
        }
    )


# ============================================================
# ROUTERS
# ============================================================

# Include API routers with prefixes
app.include_router(
    compiler.router,
    prefix="/api/v1/compiler",
    tags=["compiler"]
)

app.include_router(
    policies.router,
    prefix="/api/v1/policies",
    tags=["policies"]
)

app.include_router(
    files.router,
    prefix="/api/v1/files",
    tags=["files"]
)

app.include_router(
    enforcement.router,
    prefix="/api/v1/enforcement",
    tags=["enforcement"]
)

app.include_router(
    admin.router,
    prefix="/api/v1/admin",
    tags=["admin"]
)


# ============================================================
# ROOT ENDPOINTS
# ============================================================

@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint - redirect to docs."""
    return {
        "message": "RPL Compiler API",
        "version": app.version,
        "docs": "/api/docs"
    }


@app.get("/api/health", tags=["health"])
async def health_check():
    """
    Health check endpoint for load balancers and monitoring.
    Returns service status and dependency health.
    """
    from infrastructure.database import check_db_health
    from infrastructure.cache import check_cache_health

    # Check dependencies
    db_healthy = await check_db_health()
    cache_healthy = await check_cache_health()

    overall_healthy = db_healthy and cache_healthy

    response = {
        "status": "healthy" if overall_healthy else "degraded",
        "timestamp": time.time(),
        "version": app.version,
        "dependencies": {
            "database": "up" if db_healthy else "down",
            "cache": "up" if cache_healthy else "down"
        }
    }

    status_code = (
        status.HTTP_200_OK if overall_healthy
        else status.HTTP_503_SERVICE_UNAVAILABLE
    )

    return JSONResponse(content=response, status_code=status_code)


@app.get("/api/ready", tags=["health"])
async def readiness_check():
    """
    Readiness check for Kubernetes.
    Returns whether service is ready to accept traffic.
    """
    # Perform quick checks
    return {"status": "ready"}


@app.get("/api/metrics", tags=["monitoring"])
async def metrics():
    """
    Prometheus metrics endpoint.
    Returns metrics in Prometheus format.
    """
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    from fastapi.responses import Response

    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Development only
        log_level="info"
    )