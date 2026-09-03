"""
services — reference table for the four simulated services
(user-service, order-service, payment-service, inventory-service).

Everything else (logs, metrics, traces, deployments, incidents...)
foreign-keys to this table rather than storing the service name as a
free-text string everywhere, so a rename/typo can't silently split
one service's data into two.
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    logs: Mapped[list["Log"]] = relationship(back_populates="service")  # noqa: F821
    metrics: Mapped[list["Metric"]] = relationship(back_populates="service")  # noqa: F821
    traces: Mapped[list["Trace"]] = relationship(back_populates="service")  # noqa: F821
    deployments: Mapped[list["Deployment"]] = relationship(back_populates="service")  # noqa: F821
    code_changes: Mapped[list["CodeChange"]] = relationship(back_populates="service")  # noqa: F821
    incidents: Mapped[list["Incident"]] = relationship(back_populates="service")  # noqa: F821
    historical_incidents: Mapped[list["HistoricalIncident"]] = relationship(  # noqa: F821
        back_populates="service"
    )
    runbooks: Mapped[list["Runbook"]] = relationship(back_populates="service")  # noqa: F821

    def __repr__(self) -> str:
        return f"<Service id={self.id} name={self.name!r}>"
