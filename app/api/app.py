import structlog
from fastapi import FastAPI
from starlette import status
from starlette.requests import Request

from app.api.routers.client_db_api import client_db_router
from app.api.routers.mock_api import mock_router
from app.api.routers.rest_explorer_api import rest_router
from app.api.routers.rpl_editor_api import rpl_router
from app.api.routers.simulation_api import simulation_router
from app.api.utils.config import Config
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.api.routers.auth_api import auth_router
from app.api.routers.user_api import user_router
from prometheus_client import make_asgi_app
from app.api.database.database import init_db
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from fastapi.exceptions import RequestValidationError
from app.api.utils.logging_config import setup_logging
from app.api.utils.cache import init_cache, close_cache
from app.api.routers.resource_api import resource_router
from app.api.routers.file_manager_api import file_manager_router
from app.api.middlewares.metrics import PrometheusMetrics, PrometheusMiddleware


setup_logging()
logger = structlog.get_logger(__name__)

# Initialize metrics
prometheus_metrics = PrometheusMetrics()


@asynccontextmanager
async def lifespan(api: FastAPI):
    """
    Lifecycle manager for startup and shutdown events.
    Handles client_db connections, cache, and other resources.
    """
    # Startup
    logger.info("application_starting")

    try:
        # Initialize client_db
        await init_db()
        logger.info("database_initialized")

        # Initialize cache
        await init_cache()
        logger.info("cache_initialized")

        # Initialize metrics
        prometheus_metrics.setup()
        logger.info("metrics_initialized")

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




app.add_middleware(GZipMiddleware, minimum_size=1000)

# Metrics collection
app.add_middleware(PrometheusMiddleware)
app.mount("/metrics",make_asgi_app())



# app.add_middleware(CSRFMiddleware)
# app.add_middleware(LoggingMiddleware)
# app.add_middleware(RateLimitMiddleware)
# app.add_middleware(ErrorHandlingMiddleware)



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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[Config().get("CLIENT_ORIGIN")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(file_manager_router)
app.include_router(simulation_router)
app.include_router(resource_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(rpl_router)


app.include_router(mock_router)
app.include_router(rest_router)
app.include_router(client_db_router)
