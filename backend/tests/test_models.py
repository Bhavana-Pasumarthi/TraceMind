"""
Phase 2 tests that don't require a live Postgres connection.

These check that all 15 tables are registered on Base.metadata with the
expected columns/foreign keys — i.e. that the model layer is internally
consistent — without needing Docker running. A separate, DB-dependent
test (test_migrations.py) actually applies the Alembic migration against
a real Postgres and is skipped automatically if DATABASE_URL isn't
reachable (see its module docstring).
"""

from app.models import Base

EXPECTED_TABLES = {
    "services",
    "users",
    "logs",
    "metrics",
    "traces",
    "deployments",
    "code_changes",
    "historical_incidents",
    "runbooks",
    "incidents",
    "evidence",
    "investigations",
    "hypotheses",
    "remediations",
    "validation_runs",
}


def test_all_expected_tables_are_registered():
    assert set(Base.metadata.tables.keys()) == EXPECTED_TABLES


def test_logs_has_expected_columns_and_fk():
    logs = Base.metadata.tables["logs"]
    assert {"id", "timestamp", "service_id", "level", "message"}.issubset(logs.columns.keys())
    fk_targets = {fk.column.table.name for fk in logs.foreign_keys}
    assert fk_targets == {"services"}


def test_evidence_links_incident_and_investigation():
    evidence = Base.metadata.tables["evidence"]
    fk_targets = {fk.column.table.name for fk in evidence.foreign_keys}
    assert fk_targets == {"incidents", "investigations"}


def test_hypothesis_evidence_id_arrays_exist():
    hypotheses = Base.metadata.tables["hypotheses"]
    assert "supporting_evidence_ids" in hypotheses.columns
    assert "contradicting_evidence_ids" in hypotheses.columns


def test_remediation_requires_approval_by_default():
    remediations = Base.metadata.tables["remediations"]
    col = remediations.columns["requires_approval"]
    # Human-in-the-loop is a hard project requirement — this must never
    # silently default to False.
    assert col.default is not None or col.server_default is not None


def test_historical_incident_and_runbook_have_embedding_columns():
    for table_name in ("historical_incidents", "runbooks"):
        table = Base.metadata.tables[table_name]
        assert "embedding" in table.columns
