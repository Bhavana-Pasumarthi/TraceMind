"""
deployments — one row per deploy of a service.

The Deployment/Code Agent (Phase 9) checks temporal proximity between a
deployment and an incident's start time, but per the project rules it
must NOT claim causality from timing alone — that reasoning lives in the
agent, not here; this table just stores the facts.
"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Deployment(Base):
    __tablename__ = "deployments"
    __table_args__ = (Index("ix_deployments_service_timestamp", "service_id", "timestamp"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    version: Mapped[str] = mapped_column(String(50))
    commit_id: Mapped[str] = mapped_column(String(100))
    change_summary: Mapped[str] = mapped_column(String(1000))

    service: Mapped["Service"] = relationship(back_populates="deployments")  # noqa: F821
    code_changes: Mapped[list["CodeChange"]] = relationship(  # noqa: F821
        back_populates="deployment"
    )

    def __repr__(self) -> str:
        return f"<Deployment id={self.id} service_id={self.service_id} version={self.version!r}>"
