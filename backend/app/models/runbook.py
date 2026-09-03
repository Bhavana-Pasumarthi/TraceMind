"""
runbooks — Markdown troubleshooting docs, the other RAG target besides
historical incidents. `service_id` is nullable because some runbooks are
general (e.g. "escalation procedure") rather than service-specific.
"""

from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.historical_incident import EMBEDDING_DIM


class Runbook(Base):
    __tablename__ = "runbooks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(300))
    content_md: Mapped[str] = mapped_column(Text)
    service_id: Mapped[int | None] = mapped_column(ForeignKey("services.id"), nullable=True)
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(EMBEDDING_DIM), nullable=True
    )

    service: Mapped["Service | None"] = relationship(back_populates="runbooks")

    def __repr__(self) -> str:
        return f"<Runbook id={self.id} title={self.title!r}>"
