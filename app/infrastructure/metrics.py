
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from typing import Callable, Any
from functools import wraps
import time
import structlog

logger = structlog.get_logger(__name__)

# Prometheus metrics
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

cache_hits = Counter(
    'cache_hits_total',
    'Total cache hits'
)

cache_misses = Counter(
    'cache_misses_total',
    'Total cache misses'
)

active_connections = Gauge(
    'active_connections',
    'Number of active connections'
)


class PrometheusMetrics:
    """Prometheus metrics collector."""

    def __init__(self):
        self.initialized = False

    def setup(self):
        """Setup metrics."""
        self.initialized = True
        logger.info("prometheus_metrics_initialized")

    def record_request(self, method: str, endpoint: str, status: int, duration: float):
        """Record HTTP request metrics."""
        request_counter.labels(method=method, endpoint=endpoint, status=status).inc()
        request_duration.labels(method=method, endpoint=endpoint).observe(duration)

    def record_compilation(self, status: str, duration: float):
        """Record compilation metrics."""
        compilation_counter.labels(status=status).inc()
        compilation_duration.observe(duration)

    def record_enforcement(self, policy_id: str, decision: str, duration: float):
        """Record enforcement metrics."""
        enforcement_counter.labels(policy_id=policy_id, decision=decision).inc()
        enforcement_duration.observe(duration)

    def record_cache_hit(self):
        """Record cache hit."""
        cache_hits.inc()

    def record_cache_miss(self):
        """Record cache miss."""
        cache_misses.inc()


# Middleware for metrics collection
async def metrics_middleware(request, call_next):
    """Middleware to collect request metrics."""
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    # Record metrics
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


def track_request_metrics(operation: str):
    """Decorator to track operation metrics."""

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                logger.debug(
                    "operation_completed",
                    operation=operation,
                    duration_ms=round(duration * 1000, 2)
                )
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(
                    "operation_failed",
                    operation=operation,
                    duration_ms=round(duration * 1000, 2),
                    error=str(e)
                )
                raise

        return wrapper

    return decorator


# Simple in-memory metrics (for testing without Prometheus)
_metrics = {
    "total_requests": 0,
    "successful_requests": 0,
    "failed_requests": 0,
    "total_compilations": 0,
    "successful_compilations": 0,
    "total_enforcements": 0,
    "allowed_enforcements": 0,
    "denied_enforcements": 0,
    "cache_hit_rate": 0.0,
    "avg_response_time": 0.0,
    "avg_compilation_time": 0.0,
    "avg_enforcement_time": 0.0
}


def get_metrics() -> dict:
    """Get current metrics."""
    return _metrics.copy()


def update_metric(key: str, value: Any):
    """Update a metric value."""
    _metrics[key] = value


def increment_metric(key: str, amount: int = 1):
    """Increment a metric counter."""
    _metrics[key] = _metrics.get(key, 0) + amount