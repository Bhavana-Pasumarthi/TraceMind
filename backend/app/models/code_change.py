"""
code_changes — file-level change metadata, usually tied to a deployment.

`deployment_id` is nullable: a commit can be recorded even if we don't
(yet) know which deployment shipped it, but in practice the generator
(Phase 5) will always set it since deployments and code changes are
created together for a given scenario.
"""

from sqlalchemy import Enum, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
import enum


class ChangeType(str, enum.Enum):
    ADDED = "added"
    MODIFIED = "modified"
    REMOVED = "removed"
    CONFIG = "config"


class CodeChange(Base):
    __tablename__ = "code_changes"
    __table_args__ = (Index("ix_code_changes_service_commit", "service_id", "commit_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    commit_id: Mapped[str] = mapped_column(String(100), index=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    deployment_id: Mapped[int | None] = mapped_column(
        ForeignKey("deployments.id"), nullable=True
    )
    changed_file: Mapped[str] = mapped_column(String(500))
    change_type: Mapped[ChangeType] = mapped_column(Enum(ChangeType, name="change_type"))
    change_summary: Mapped[str] = mapped_column(String(1000))

    service: Mapped["Service"] = relationship(back_populates="code_changes")  # noqa: F821
    deployment: Mapped["Deployment | None"] = relationship(back_populates="code_changes")

    def __repr__(self) -> str:
        return f"<CodeChange id={self.id} commit_id={self.commit_id!r} file={self.changed_file!r}>"
