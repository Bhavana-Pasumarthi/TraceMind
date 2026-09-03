"""
validation_runs — the outcome of actually applying an approved
remediation inside the sandbox (Phase 12) and re-running tests.

`tests_run_json` / `results_json` store structured detail so the
frontend can show exactly what was tested, not just pass/fail — and so
Phase 13's evaluator can compute remediation-validation success rate
from real recorded outcomes rather than inferring it.
"""

from datetime import datetime

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import ValidationStatus


class ValidationRun(Base):
    __tablename__ = "validation_runs"

    id: Mapped[int] = mapped_column(primary_key=True)
    remediation_id: Mapped[int] = mapped_column(ForeignKey("remediations.id"))
    status: Mapped[ValidationStatus] = mapped_column(
        Enum(ValidationStatus, name="validation_status"), default=ValidationStatus.NOT_VALIDATED
    )
    tests_run_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    results_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    remediation: Mapped["Remediation"] = relationship(back_populates="validation_runs")

    def __repr__(self) -> str:
        return f"<ValidationRun id={self.id} status={self.status}>"
