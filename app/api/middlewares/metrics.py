from prometheus_client import Counter, Histogram, Gauge
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import structlog
import time
from typing import Callable

logger = structlog.get_logger(__name__)

# ------------------------------------------------------------------------------
# Prometheus Metrics
# ------------------------------------------------------------------------------

request_counter = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

compilation_counter = Counter(
    'compilations_total',
    'Total compilations',
    ['status']
)

compilation_duration = Histogram(
    'compilation_duration_seconds',
    'Compilation duration'
)

enforcement_counter = Counter(
    'enforcements_total',
    'Total enforcement checks',
    ['policy_id', 'decision']
)

enforcement_duration = Histogram(
    'enforcement_duration_seconds',
    'Enforcement check duration'
)

active_connections = Gauge(
    'active_connections',
    'Number of active connections'
)

cache_hits = Counter(
    'cache_hits_total',
    'Total cache hits'
)

cache_misses = Counter(
    'cache_misses_total',
    'Total cache misses'
)


class PrometheusMetrics:
    """Prometheus metrics collector."""

    def __init__(self):
        self.initialized = False

    def setup(self):
        """Mark metrics as initialized."""
        self.initialized = True
        logger.info("prometheus_metrics_initialized")

    # --- metric recording helpers ---

    @staticmethod
    def record_request(self, method: str, endpoint: str, status: int, duration: float):
        request_counter.labels(method=method, endpoint=endpoint, status=status).inc()
        request_duration.labels(method=method, endpoint=endpoint).observe(duration)

    @staticmethod
    def record_compilation(self, status: str, duration: float):
        compilation_counter.labels(status=status).inc()
        compilation_duration.observe(duration)

    @staticmethod
    def record_enforcement(self, policy_id: str, decision: str, duration: float):
        enforcement_counter.labels(policy_id=policy_id, decision=decision).inc()
        enforcement_duration.observe(duration)

    @staticmethod
    def record_cache_hit(self):
        cache_hits.inc()

    @staticmethod
    def record_cache_miss(self):
        cache_misses.inc()


# ------------------------------------------------------------------------------
# FastAPI Middleware (Class-based)
# ------------------------------------------------------------------------------

class PrometheusMiddleware(BaseHTTPMiddleware):
    """Middleware to collect HTTP metrics for FastAPI."""

    async def dispatch(self, request: Request, call_next: Callable):
        start = time.time()
        active_connections.inc()

        try:
            response = await call_next(request)
        finally:
            active_connections.dec()

        duration = time.time() - start

        request_counter.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()

        request_duration.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)

        return response


