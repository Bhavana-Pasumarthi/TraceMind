"""
investigations — one row per "Investigate this incident" run.

`plan_json` stores the Orchestrator's plan (Phase 9) — which evidence
sources it decided were relevant and why. Kept structured (not just a
log line) so the frontend can show "here's what TraceMind decided to
look at" as part of the explainability story.
"""

from datetime import datetime

from sqlalchemy import JSON, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import InvestigationStatus


class Investigation(Base):
    __tablename__ = "investigations"

    id: Mapped[int] = mapped_column(primary_key=True)
    incident_id: Mapped[int] = mapped_column(ForeignKey("incidents.id"))
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[InvestigationStatus] = mapped_column(
        Enum(InvestigationStatus, name="investigation_status"),
        default=InvestigationStatus.PENDING,
    )
    plan_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    incident: Mapped["Incident"] = relationship(back_populates="investigations")
    evidence_items: Mapped[list["Evidence"]] = relationship(back_populates="investigation")
    hypotheses: Mapped[list["Hypothesis"]] = relationship(back_populates="investigation")

    def __repr__(self) -> str:
        return f"<Investigation id={self.id} incident_id={self.incident_id} status={self.status}>"
