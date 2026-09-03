"""
users — minimal identity table.

Not a full auth system (Phase 1-8 has no auth requirement per the plan).
Exists mainly so `remediations.approved_by` can reference a real person
rather than a free-text name, since human approval of remediation is a
hard project requirement (never auto-apply changes).
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(String(50), default="engineer")

    def __repr__(self) -> str:
        return f"<User id={self.id} name={self.name!r}>"
