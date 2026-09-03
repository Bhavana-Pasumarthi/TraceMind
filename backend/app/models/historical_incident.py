"""
historical_incidents — the knowledge base the Historical Incident Agent
(Phase 9) does pgvector similarity search over.

`embedding` is populated in Phase 8 (RAG pipeline: chunk → embed →
store). Dimension 1536 matches common embedding model output size
(e.g. OpenAI text-embedding-3-small); this is a config constant, not
hard-coded logic, so it can change if the embedding model changes —
see docs/data-model.md once Phase 8 lands.
"""

from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import Severity

EMBEDDING_DIM = 1536


class HistoricalIncident(Base):
    __tablename__ = "historical_incidents"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(300))
    severity: Mapped[Severity] = mapped_column(Enum(Severity, name="historical_incident_severity"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    environment: Mapped[str] = mapped_column(String(50), default="production")
    symptoms: Mapped[str] = mapped_column(Text)
    root_cause: Mapped[str] = mapped_column(Text)
    resolution: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(EMBEDDING_DIM), nullable=True
    )

    service: Mapped["Service"] = relationship(back_populates="historical_incidents")  # noqa: F821

    def __repr__(self) -> str:
        return f"<HistoricalIncident id={self.id} title={self.title!r}>"
