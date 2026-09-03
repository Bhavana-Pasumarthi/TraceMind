"""
logs — application log lines produced by the simulator (Phase 4+).

Indexed on (service_id, timestamp) because almost every query in this
system is "give me this service's data in this time window" — that's
how the Log Agent's tool call is shaped (Phase 9), and how the frontend
timeline view queries too (Phase 6/12).
"""

from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import LogLevel


class Log(Base):
    __tablename__ = "logs"
    __table_args__ = (Index("ix_logs_service_timestamp", "service_id", "timestamp"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    environment: Mapped[str] = mapped_column(String(50), default="production")
    level: Mapped[LogLevel] = mapped_column(Enum(LogLevel, name="log_level"))
    endpoint: Mapped[str | None] = mapped_column(String(200), nullable=True)
    error_type: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    message: Mapped[str] = mapped_column(String(2000))
    request_id: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    trace_id: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)

    service: Mapped["Service"] = relationship(back_populates="logs")  # noqa: F821

    def __repr__(self) -> str:
        return f"<Log id={self.id} service_id={self.service_id} level={self.level}>"
