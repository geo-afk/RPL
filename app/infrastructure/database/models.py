from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Boolean, DateTime, JSON, Integer, Float, Text
from datetime import datetime, UTC
import structlog

logger = structlog.get_logger(__name__)

# SQLAlchemy base
Base = declarative_base()



# Database models
class PolicyModel(Base):
    """SQLAlchemy model for policies."""
    __tablename__ = "policies"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    version = Column(String, default="1.0.0")
    code = Column(Text, nullable=False)
    compiled = Column(Boolean, default=False)
    enabled = Column(Boolean, default=True)

    compilation_result = Column(JSON, nullable=True)
    tags = Column(JSON, default=list)

    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, efault=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    created_by = Column(String, nullable=True)

    total_enforcements = Column(Integer, default=0)
    last_enforced_at = Column(DateTime, nullable=True)


class FileModel(Base):
    """SQLAlchemy model for files."""
    __tablename__ = "files"

    id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    content_type = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    tags = Column(JSON, default=list)

    storage_path = Column(String, nullable=False)
    processed = Column(Boolean, default=False)
    policy_id = Column(String, nullable=True)

    uploaded_at = Column(DateTime, default=lambda: datetime.now(UTC))
    uploaded_by = Column(String, nullable=True)


class EnforcementLogModel(Base):
    """SQLAlchemy model for enforcement logs."""
    __tablename__ = "enforcement_logs"

    id = Column(String, primary_key=True)
    policy_id = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    action = Column(String, nullable=False)
    resource = Column(String, nullable=False)
    allowed = Column(Boolean, nullable=False)

    matched_rules = Column(JSON, default=list)
    context = Column(JSON, default=dict)
    reason = Column(Text, nullable=False)

    timestamp = Column(DateTime, default=lambda: datetime.now(UTC))
    evaluation_time_ms = Column(Float, nullable=True)
    request_id = Column(String, nullable=True)

