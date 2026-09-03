"""
metrics — one row per (service, timestamp) sample.

Stored as plain numeric columns rather than a generic key/value table —
the Metrics Agent's anomaly-detection logic (Phase 9) needs to do real
arithmetic (thresholds, rolling averages) on these, which is awkward and
slow against an EAV-style schema. A fixed, known set of metric columns
is the right tradeoff for this project's scope.
"""

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Metric(Base):
    __tablename__ = "metrics"
    __table_args__ = (Index("ix_metrics_service_timestamp", "service_id", "timestamp"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    cpu_usage: Mapped[float] = mapped_column(Float)  # percentage 0-100
    memory_usage: Mapped[float] = mapped_column(Float)  # percentage 0-100
    request_count: Mapped[int] = mapped_column(Integer)
    error_rate: Mapped[float] = mapped_column(Float)  # percentage 0-100
    latency_ms: Mapped[float] = mapped_column(Float)
    db_connections: Mapped[int] = mapped_column(Integer)
    queue_length: Mapped[int] = mapped_column(Integer)

    service: Mapped["Service"] = relationship(back_populates="metrics")  # noqa: F821

    def __repr__(self) -> str:
        return f"<Metric id={self.id} service_id={self.service_id} timestamp={self.timestamp}>"
