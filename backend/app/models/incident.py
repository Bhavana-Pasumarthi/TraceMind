"""
incidents — the central row a user selects to investigate.

`scenario_id` links back to the failure scenario that generated this
incident (Phase 5) — used only by the evaluation harness (Phase 13) to
look up ground truth; it is NOT exposed to the agent pipeline, per the
project's evaluation-integrity requirement (ground truth must never
reach the AI during evaluation).
"""

from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import IncidentStatus, Severity


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(300))
    severity: Mapped[Severity] = mapped_column(Enum(Severity, name="incident_severity"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    environment: Mapped[str] = mapped_column(String(50), default="production")
    status: Mapped[IncidentStatus] = mapped_column(
        Enum(IncidentStatus, name="incident_status"), default=IncidentStatus.OPEN
    )
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    scenario_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    service: Mapped["Service"] = relationship(back_populates="incidents")  # noqa: F821
    evidence_items: Mapped[list["Evidence"]] = relationship(back_populates="incident")
    investigations: Mapped[list["Investigation"]] = relationship(back_populates="incident")

    def __repr__(self) -> str:
        return f"<Incident id={self.id} title={self.title!r} status={self.status}>"
