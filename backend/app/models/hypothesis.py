"""
hypotheses — ranked root-cause candidates produced by the Root Cause
Analysis stage (Phase 10).

`supporting_evidence_ids` / `contradicting_evidence_ids` are Postgres
arrays of `evidence.id` — every hypothesis must cite real evidence rows,
never free-text claims, per the project's evidence-grounding requirement
(this is also what the Phase 13 evaluator checks programmatically:
that cited IDs actually exist and actually support the claim).
`confidence` is explicitly documented as model/system confidence, not
ground truth — see docs/agent-design.md once Phase 10 lands.
"""

from sqlalchemy import ARRAY, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Hypothesis(Base):
    __tablename__ = "hypotheses"

    id: Mapped[int] = mapped_column(primary_key=True)
    investigation_id: Mapped[int] = mapped_column(ForeignKey("investigations.id"))
    hypothesis_text: Mapped[str] = mapped_column(String(1000))
    confidence: Mapped[float] = mapped_column(Float)  # system confidence, 0.0-1.0 — not ground truth
    supporting_evidence_ids: Mapped[list[int]] = mapped_column(ARRAY(Integer), default=list)
    contradicting_evidence_ids: Mapped[list[int]] = mapped_column(ARRAY(Integer), default=list)
    reasoning_summary: Mapped[str] = mapped_column(Text)
    rank: Mapped[int] = mapped_column(Integer)  # 1 = leading hypothesis

    investigation: Mapped["Investigation"] = relationship(back_populates="hypotheses")
    remediations: Mapped[list["Remediation"]] = relationship(back_populates="hypothesis")

    def __repr__(self) -> str:
        return f"<Hypothesis id={self.id} rank={self.rank} confidence={self.confidence}>"
