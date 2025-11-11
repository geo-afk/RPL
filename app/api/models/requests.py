from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator
from app.api.models.enums import CompilationMode, PolicyAction
from datetime import datetime

# ============================================================
# COMPILATION REQUESTS
# ============================================================

class CompileRequest(BaseModel):
    """Request to compile SPL code."""

    code: str = Field(
        ...,
        description="RPL source code to compile",
        min_length=1,
        max_length=1_000_000  # 1MB limit
    )

    mode: CompilationMode = Field(
        default=CompilationMode.FULL,
        description="Compilation mode"
    )

    enable_llm_analysis: bool = Field(
        default=True,
        description="Enable LLM security analysis"
    )

    generate_code: bool = Field(
        default=True,
        description="Generate executable target code"
    )

    optimization_level: int = Field(
        default=1,
        ge=0,
        le=3,
        description="Code optimization level (0-3)"
    )

    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional metadata"
    )

    @field_validator('code')
    @classmethod
    def validate_code(cls, v: str) -> str:
        """Validate and sanitize code input."""
        # Strip excessive whitespace
        v = v.strip()

        # Check for forbidden patterns (basic security)
        forbidden = ['__import__', 'exec(', 'eval(', 'compile(']
        for pattern in forbidden:
            if pattern in v:
                raise ValueError(f"Forbidden pattern detected: {pattern}")

        return v

    class Config:
        json_schema_extra = {
            "example": {
                "code": "ROLE Admin {can: read, write}\nUSER Alice {role: Admin}",
                "mode": "full",
                "enable_llm_analysis": True,
                "generate_code": True,
                "optimization_level": 1
            }
        }


class ValidateRequest(BaseModel):
    """Request to validate SPL code without full compilation."""

    code: str = Field(..., description="SPL code to validate")

    strict: bool = Field(
        default=True,
        description="Enable strict validation rules"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "code": "ROLE Admin {can: read}",
                "strict": True
            }
        }


# ============================================================
# POLICY ENFORCEMENT REQUESTS
# ============================================================

class EnforcementRequest(BaseModel):
    """Request to check policy enforcement."""

    policy_id: str = Field(
        ...,
        description="ID of compiled policy to use"
    )

    subject: str = Field(
        ...,
        description="User or role making the request"
    )

    action: PolicyAction = Field(
        ...,
        description="Action to perform"
    )

    resource: str = Field(
        ...,
        description="Resource being accessed"
    )

    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional context (time, IP, device, etc.)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "policy_id": "policy_123",
                "subject": "Alice",
                "action": "read",
                "resource": "DB_Finance",
                "context": {
                    "ip_address": "192.168.1.100",
                    "time": "2025-11-07T14:30:00Z",
                    "device": "laptop"
                }
            }
        }


class BatchEnforcementRequest(BaseModel):
    """Request to check multiple policy decisions."""

    policy_id: str

    requests: List[EnforcementRequest] = Field(
        ...,
        max_length=100,  # Limit batch size
        description="List of enforcement requests"
    )


# ============================================================
# FILE OPERATION REQUESTS
# ============================================================

class FileUploadMetadata(BaseModel):
    """Metadata for file uploads."""

    filename: str = Field(..., description="Original filename")

    content_type: str = Field(
        default="text/plain",
        description="File content type"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="File description"
    )

    tags: Optional[List[str]] = Field(
        default=None,
        max_length=10,
        description="Tags for categorization"
    )

    auto_compile: bool = Field(
        default=False,
        description="Automatically compile after upload"
    )


class FileQueryParams(BaseModel):
    """Query parameters for file listing."""

    skip: int = Field(default=0, ge=0, description="Number of records to skip")
    limit: int = Field(default=20, ge=1, le=100, description="Max records to return")
    tags: Optional[List[str]] = Field(default=None, description="Filter by tags")
    search: Optional[str] = Field(default=None, description="Search query")
    sort_by: Literal["created_at", "filename", "size"] = Field(
        default="created_at",
        description="Sort field"
    )
    sort_order: Literal["asc", "desc"] = Field(
        default="desc",
        description="Sort order"
    )


# ============================================================
# POLICY MANAGEMENT REQUESTS
# ============================================================

class PolicyCreateRequest(BaseModel):
    """Request to create a new policy."""

    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    code: str = Field(..., description="SPL code")
    version: str = Field(default="1.0.0", description="Policy version")
    tags: Optional[List[str]] = Field(default=None)
    enabled: bool = Field(default=True, description="Policy active status")


class PolicyUpdateRequest(BaseModel):
    """Request to update an existing policy."""

    name: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    code: Optional[str] = Field(default=None)
    version: Optional[str] = Field(default=None)
    tags: Optional[List[str]] = Field(default=None)
    enabled: Optional[bool] = Field(default=None)


class PolicyQueryParams(BaseModel):
    """Query parameters for policy listing."""

    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)
    enabled: Optional[bool] = Field(default=None)
    tags: Optional[List[str]] = Field(default=None)
    search: Optional[str] = Field(default=None)
    version: Optional[str] = Field(default=None)


# ============================================================
# RESPONSE MODELS
# ============================================================

class CompilationResult(BaseModel):
    """Result of compilation."""

    success: bool
    policy_id: Optional[str] = None

    # Compilation phases
    lexical_analysis: Dict[str, Any] = Field(default_factory=dict)
    syntax_analysis: Dict[str, Any] = Field(default_factory=dict)
    semantic_analysis: Dict[str, Any] = Field(default_factory=dict)

    # Results
    tokens: Optional[List[Dict[str, Any]]] = None
    parse_tree: Optional[str] = None
    symbol_table: Optional[Dict[str, Any]] = None

    # Code generation
    generated_code: Optional[str] = None

    # LLM analysis
    security_findings: Optional[List[Dict[str, Any]]] = None
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
                "warnings": ["Potential overly permissive rule at line 5"],
                "risk_score": 3.5,
                "compilation_time_ms": 125.4
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
    """Policy information response."""

    id: str
    name: str
    description: Optional[str]
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
    """File information response."""

    id: str
    filename: str
    size: int
    content_type: str
    description: Optional[str]
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


class ErrorResponse(BaseModel):
    """Error response format."""

    error: str
    message: str
    details: Optional[Any] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HealthResponse(BaseModel):
    """Health check response."""

    status: Literal["healthy", "degraded", "unhealthy"]
    version: str
    timestamp: float
    dependencies: Dict[str, str]