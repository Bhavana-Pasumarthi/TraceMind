"""
Applies the Alembic migration against DATABASE_URL and checks the
resulting schema. Requires the `db` service actually running
(`docker compose up db`) — this sandbox has no network access to do
that, so this test was written but not executed here. It self-skips if
Postgres isn't reachable so `pytest` doesn't hard-fail in environments
without the DB up (e.g. a quick `pytest tests/test_models.py` pass).

Run for real with:
    docker compose up -d db
    cd backend && alembic upgrade head && pytest tests/test_migrations.py -v
"""

import pytest
from sqlalchemy import create_engine, inspect, text

from app.config import get_settings

settings = get_settings()


def _db_reachable() -> bool:
    try:
        engine = create_engine(settings.database_url, connect_args={"connect_timeout": 2})
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not _db_reachable(), reason="Postgres not reachable at DATABASE_URL — start it with `docker compose up db`"
)


def test_migration_creates_all_tables():
    from app.models import Base

    engine = create_engine(settings.database_url)
    inspector = inspect(engine)
    actual_tables = set(inspector.get_table_names())
    expected_tables = set(Base.metadata.tables.keys())
    assert expected_tables.issubset(actual_tables), (
        f"Missing tables: {expected_tables - actual_tables}. "
        "Did you run `alembic upgrade head`?"
    )


def test_pgvector_extension_is_enabled():
    engine = create_engine(settings.database_url)
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT extname FROM pg_extension WHERE extname = 'vector'")
        ).fetchone()
    assert result is not None, "pgvector extension is not enabled"
