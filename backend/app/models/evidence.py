"""
evidence — every piece of information an investigation surfaced,
tagged FACT or EVIDENCE (never a bare hypothesis — those live in
`hypotheses`, and always cite evidence rows by ID, never free text).

`source_type` + `source_ref_id` point back at the original row (a log,
a metric, a trace, a deployment, a historical incident, a runbook chunk)
so the frontend's "click an evidence ID to see the original" feature
(a hard project requirement) has something concrete to resolve.
`payload_json` stores a denormalized snapshot of that source row at
collection time — useful even if the underlying row's rendering logic
changes later, and avoids N+1 joins across five different tables when
rendering an investigation.
"""

from datetime import datetime

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import EvidenceCategory


class Evidence(Base):
    __tablename__ = "evidence"

    id: Mapped[int] = mapped_column(primary_key=True)
    incident_id: Mapped[int] = mapped_column(ForeignKey("incidents.id"))
    investigation_id: Mapped[int | None] = mapped_column(
        ForeignKey("investigations.id"), nullable=True
    )
    source_type: Mapped[str] = mapped_column(String(50))  # "log" | "metric" | "trace" | ...
    source_ref_id: Mapped[int] = mapped_column()  # PK of the row in its source table
    label: Mapped[str] = mapped_column(String(300))
    category: Mapped[EvidenceCategory] = mapped_column(
        Enum(EvidenceCategory, name="evidence_category")
    )
    payload_json: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    incident: Mapped["Incident"] = relationship(back_populates="evidence_items")
    investigation: Mapped["Investigation | None"] = relationship(back_populates="evidence_items")

    def __repr__(self) -> str:
        return f"<Evidence id={self.id} source_type={self.source_type!r} category={self.category}>"
