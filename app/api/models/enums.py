from enum import Enum


# ============================================================
# ENUMS
# ============================================================

class PolicyAction(str, Enum):
    """Allowed policy actions."""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    EXECUTE = "execute"
    ALL = "*"


class PolicyType(str, Enum):
    """Policy rule types."""
    ALLOW = "ALLOW"
    DENY = "DENY"


class CompilationMode(str, Enum):
    """Compilation modes."""
    FULL = "full"  # Full compilation with all phases
    VALIDATE = "validate"  # Only validation
    ANALYZE = "analyze"  # Only security analysis
    PARSE = "parse"  # Only parsing

