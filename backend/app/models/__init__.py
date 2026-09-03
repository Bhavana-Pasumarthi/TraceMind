"""
Importing this module registers every ORM model on `Base.metadata`.

Alembic's `env.py` imports `app.models` (not individual model files) so
`target_metadata = Base.metadata` sees the complete schema for
autogeneration. If you add a new model file, import it here too, or
Alembic will silently not know it exists.
"""

from app.models.base import Base
from app.models.service import Service
from app.models.user import User
from app.models.log import Log
from app.models.metric import Metric
from app.models.trace import Trace
from app.models.deployment import Deployment
from app.models.code_change import CodeChange
from app.models.historical_incident import HistoricalIncident
from app.models.runbook import Runbook
from app.models.incident import Incident
from app.models.evidence import Evidence
from app.models.investigation import Investigation
from app.models.hypothesis import Hypothesis
from app.models.remediation import Remediation
from app.models.validation_run import ValidationRun

__all__ = [
    "Base",
    "Service",
    "User",
    "Log",
    "Metric",
    "Trace",
    "Deployment",
    "CodeChange",
    "HistoricalIncident",
    "Runbook",
    "Incident",
    "Evidence",
    "Investigation",
    "Hypothesis",
    "Remediation",
    "ValidationRun",
]
