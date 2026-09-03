"""
traces — spans representing a request's path across services.

Multiple rows share a trace_id (one request chain, e.g. order-service
calling payment-service calling Postgres) — that's how the Trace Agent
(Phase 9) reconstructs the request path and finds bottleneck spans.
"""

from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import TraceStatus


class Trace(Base):
    __tablename__ = "traces"
    __table_args__ = (
        Index("ix_traces_trace_id", "trace_id"),
        Index("ix_traces_service_start_time", "service_id", "start_time"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    trace_id: Mapped[str] = mapped_column(String(100))
    request_id: Mapped[str] = mapped_column(String(100), index=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    operation: Mapped[str] = mapped_column(String(200))
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    duration_ms: Mapped[float] = mapped_column(Float)
    status: Mapped[TraceStatus] = mapped_column(Enum(TraceStatus, name="trace_status"))

    service: Mapped["Service"] = relationship(back_populates="traces")  # noqa: F821

    def __repr__(self) -> str:
        return f"<Trace id={self.id} trace_id={self.trace_id} service_id={self.service_id}>"
