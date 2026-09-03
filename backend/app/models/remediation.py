"""
remediations — a proposed action from the fixed remediation catalog
(Phase 11), tied to the hypothesis it addresses.

`requires_approval` is always True for anything that would touch the
sandbox — this table is the audit trail proving a human, not the AI,
authorized every validated change (`approved_by` / `approved_at`).
Nothing here executes arbitrary text; `action_type` must be one of a
small enum of predefined safe actions (see docs/agent-design.md, Phase
11) — the LLM selects and explains, it does not generate new actions.
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import RiskLevel


class Remediation(Base):
    __tablename__ = "remediations"

    id: Mapped[int] = mapped_column(primary_key=True)
    investigation_id: Mapped[int] = mapped_column(ForeignKey("investigations.id"))
    hypothesis_id: Mapped[int] = mapped_column(ForeignKey("hypotheses.id"))
    action_type: Mapped[str] = mapped_column(String(100))  # e.g. "increase_db_pool_size"
    rationale: Mapped[str] = mapped_column(Text)
    risk_level: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel, name="remediation_risk_level"))
    rollback_plan: Mapped[str] = mapped_column(Text)
    requires_approval: Mapped[bool] = mapped_column(Boolean, default=True)
    approved_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    hypothesis: Mapped["Hypothesis"] = relationship(back_populates="remediations")
    validation_runs: Mapped[list["ValidationRun"]] = relationship(back_populates="remediation")

    def __repr__(self) -> str:
        return f"<Remediation id={self.id} action_type={self.action_type!r}>"
