from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime


class TokenInfo(BaseModel):
    """Information about a single token."""
    type: str
    text: str
    line: int
    column: int


class LexicalAnalysisResponse(BaseModel):
    """Response from lexical analysis."""
    success: bool
    token_count: int
    tokens: List[TokenInfo]
    errors: List[str] = Field(default_factory=list)


class SyntaxAnalysisResponse(BaseModel):
    """Response from syntax analysis."""
    success: bool
    parse_tree: Optional[str] = None
    errors: List[str] = Field(default_factory=list)


class SemanticAnalysisResponse(BaseModel):
    """Response from semantic analysis."""
    success: bool
    symbol_table: Dict[str, Any] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class SecurityFinding(BaseModel):
    """A single security finding from LLM analysis."""
    line: Optional[int] = None
    risk_score: int = Field(..., ge=1, le=10)
    category: str
    description: str
    recommendation: str
    severity: Literal["low", "medium", "high", "critical"] = "medium"

    class Config:
        json_schema_extra = {
            "example": {
                "line": 15,
                "risk_score": 8,
                "category": "Privilege Escalation",
                "description": "Admin role has unrestricted access",
                "recommendation": "Implement least privilege principle",
                "severity": "high"
            }
        }


class CompilationResult(BaseModel):
    """Complete compilation result."""
    success: bool
    policy_id: Optional[str] = None

    # Analysis results
    lexical_analysis: Dict[str, Any] = Field(default_factory=dict)
    syntax_analysis: Dict[str, Any] = Field(default_factory=dict)
    semantic_analysis: Dict[str, Any] = Field(default_factory=dict)

    # Extracted data
    tokens: Optional[List[TokenInfo]] = None
    parse_tree: Optional[str] = None
    symbol_table: Optional[Dict[str, Any]] = None

    # Generated code
    generated_code: Optional[str] = None

    # Security analysis
    security_findings: Optional[List[SecurityFinding]] = None
    risk_score: Optional[float] = None

    # Errors and warnings
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

    # Metrics
    compilation_time_ms: Optional[float] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "policy_id": "policy_abc123",
                "errors": [],
                "warnings": ["Line 5: Overly permissive rule detected"],
                "risk_score": 4.5,
                "compilation_time_ms": 234.56
            }
        }


class EnforcementResult(BaseModel):
    """Result of policy enforcement check."""
    allowed: bool
    policy_id: str
    subject: str
    action: str
    resource: str

    # Decision details
    matched_rules: List[Dict[str, Any]] = Field(default_factory=list)
    reason: str

    # Audit info
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None

    # Performance
    evaluation_time_ms: Optional[float] = None

    class Config:
        json_schema_extra = {
            "example": {
                "allowed": False,
                "policy_id": "policy_abc123",
                "subject": "Alice",
                "action": "delete",
                "resource": "DB_Finance",
                "matched_rules": [
                    {
                        "rule_type": "DENY",
                        "line": 15,
                        "reason": "Explicit DENY for delete action"
                    }
                ],
                "reason": "Access denied by policy rule at line 15",
                "evaluation_time_ms": 2.3
            }
        }


class PolicyResponse(BaseModel):
    """Response containing policy information."""
    id: str
    name: str
    description: Optional[str] = None
    version: str
    enabled: bool

    # Code
    code: str
    compiled: bool

    # Metadata
    tags: List[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None

    # Compilation info
    compilation_result: Optional[CompilationResult] = None

    # Statistics
    total_enforcements: int = 0
    last_enforced_at: Optional[datetime] = None


class FileResponse(BaseModel):
    """Response containing file information."""
    id: str
    filename: str
    size: int
    content_type: str
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

    # Upload info
    uploaded_at: datetime
    uploaded_by: Optional[str] = None

    # Processing status
    processed: bool = False
    policy_id: Optional[str] = None

    # Download URL
    download_url: str


class PaginatedResponse(BaseModel):
    """Generic paginated response."""
    items: List[Any]
    total: int
    skip: int
    limit: int
    has_more: bool

    class Config:
        json_schema_extra = {
            "example": {
                "items": [],
                "total": 100,
                "skip": 0,
                "limit": 20,
                "has_more": True
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response format."""
    error: str
    message: str
    details: Optional[Any] = None
    request_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Invalid input data",
                "details": {"field": "code", "issue": "cannot be empty"},
                "request_id": "req_abc123",
                "timestamp": "2025-11-07T12:34:56"
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    status: Literal["healthy", "degraded", "unhealthy"]
    version: str
    timestamp: float
    uptime_seconds: Optional[float] = None
    dependencies: Dict[str, str] = Field(default_factory=dict)

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "timestamp": 1699368000.0,
                "uptime_seconds": 86400.0,
                "dependencies": {
                    "database": "up",
                    "cache": "up",
                    "llm_api": "up"
                }
            }
        }


class MetricsResponse(BaseModel):
    """Metrics response."""
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_response_time_ms: float

    # Compilation metrics
    total_compilations: int
    successful_compilations: int
    average_compilation_time_ms: float

    # Enforcement metrics
    total_enforcements: int
    allowed_enforcements: int
    denied_enforcements: int
    average_enforcement_time_ms: float

    # Cache metrics
    cache_hit_rate: float

    class Config:
        json_schema_extra = {
            "example": {
                "total_requests": 10000,
                "successful_requests": 9950,
                "failed_requests": 50,
                "average_response_time_ms": 45.6,
                "total_compilations": 500,
                "successful_compilations": 485,
                "average_compilation_time_ms": 234.5,
                "total_enforcements": 5000,
                "allowed_enforcements": 4200,
                "denied_enforcements": 800,
                "average_enforcement_time_ms": 3.2,
                "cache_hit_rate": 0.85
            }
        }


class EnforcementStatsResponse(BaseModel):
    """Statistics about policy enforcement."""
    policy_id: str
    total_checks: int
    allowed_count: int
    denied_count: int
    allow_rate: float

    # Top subjects
    top_subjects: List[Dict[str, Any]] = Field(default_factory=list)

    # Top resources
    top_resources: List[Dict[str, Any]] = Field(default_factory=list)

    # Performance
    average_evaluation_time_ms: float
    p50_evaluation_time_ms: float
    p95_evaluation_time_ms: float
    p99_evaluation_time_ms: float

    # Time range
    from_date: datetime
    to_date: datetime


class ExplanationResponse(BaseModel):
    """Detailed explanation of enforcement decision."""
    decision: Literal["allow", "deny"]
    policy_id: str
    subject: str
    action: str
    resource: str

    # Step-by-step explanation
    steps: List[Dict[str, Any]] = Field(default_factory=list)

    # All evaluated rules
    evaluated_rules: List[Dict[str, Any]] = Field(default_factory=list)

    # Final reasoning
    reasoning: str

    # Suggestions (if denied)
    suggestions: Optional[List[str]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "decision": "deny",
                "policy_id": "policy_abc123",
                "subject": "Alice",
                "action": "delete",
                "resource": "DB_Finance",
                "steps": [
                    {"step": 1, "description": "Loaded policy rules"},
                    {"step": 2, "description": "Found 3 matching rules"},
                    {"step": 3, "description": "Evaluated DENY rule at line 15"},
                    {"step": 4, "description": "DENY overrides ALLOW"}
                ],
                "reasoning": "Access denied due to explicit DENY rule",
                "suggestions": [
                    "Request role upgrade from Admin",
                    "Use a different action (read/write instead of delete)"
                ]
            }
        }