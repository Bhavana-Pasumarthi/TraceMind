"""
Shared enums.

Kept in one place so the same allowed values are enforced consistently
across logs, incidents, evidence, etc. — and so agent/tool code (Phase
9+) can import these instead of hard-coding string literals.
"""

import enum


class LogLevel(str, enum.Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class Severity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentStatus(str, enum.Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TraceStatus(str, enum.Enum):
    OK = "ok"
    ERROR = "error"


class EvidenceCategory(str, enum.Enum):
    """
    Enforces the FACT vs EVIDENCE distinction at the data layer, not just
    in prompt text — the Evidence Correlation agent (Phase 9) must tag
    every row with one of these, and the API/frontend can rely on it
    always being one of exactly two values.
    """

    FACT = "fact"
    EVIDENCE = "evidence"


class InvestigationStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ValidationStatus(str, enum.Enum):
    PASSED = "passed"
    FAILED = "failed"
    NOT_VALIDATED = "not_validated"


class RiskLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
