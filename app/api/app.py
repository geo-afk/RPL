import structlog
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request

from app.api.utils.config import Config
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.api.routers.user_api import router
from prometheus_client import make_asgi_app
from app.api.database.database import init_db
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from app.api.utils.logging_config import setup_logging
from app.api.utils.cache import init_cache, close_cache
from app.api.middlewares.logging import LoggingMiddleware
from app.api.middlewares.rate_limiting import RateLimitMiddleware
from app.api.middlewares.error_handler import ErrorHandlingMiddleware
from app.api.middlewares.metrics import PrometheusMetrics, PrometheusMiddleware

# Setup structured logging
setup_logging()
logger = structlog.get_logger(__name__)

# Initialize metrics
prometheus_metrics = PrometheusMetrics()



@asynccontextmanager
async def lifespan(api: FastAPI):
    """
    Lifecycle manager for startup and shutdown events.
    Handles database connections, cache, and other resources.
    """
    # Startup
    logger.info("application_starting")

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

        logger.info("database_closed")

        logger.info("application_shutdown_complete")


app = FastAPI(
    title="RPL Compiler API",
    description="Secure Policy Language Compiler with REST API",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[Config().get("CLIENT_ORIGIN")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(GZipMiddleware, minimum_size=1000)

# Metrics collection
app.add_middleware(PrometheusMiddleware)
app.mount("/metrics",make_asgi_app())


app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(ErrorHandlingMiddleware)



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


app.include_router(router)
