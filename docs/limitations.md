# Limitations

Updated at the end of every phase. Nothing here is claimed unless it's
actually true of the current code.

## As of Phase 2

- **Not verified against a live database.** This development environment
  has no network access, so the Alembic migration and all model
  relationships were written carefully and checked for internal
  consistency (`pytest tests/test_models.py` — passes without a DB) and
  syntax-compiled, but `alembic upgrade head` has not actually been run
  against Postgres, and `pytest tests/test_migrations.py` (which does
  that) has not been executed. **Run both before trusting this schema.**
- The initial migration (`0001_initial_schema.py`) was hand-written to
  mirror the models rather than produced by `alembic revision
  --autogenerate`, for the same network-access reason above. There is
  some risk of a small mismatch between the migration and the ORM
  models that autogenerate would have caught automatically — the
  `test_migration_creates_all_tables` test checks for this once you can
  run it, but do run it before Phase 3.
- No data exists yet. No simulator. No agents. No LLM integration.
- pgvector columns exist (`historical_incidents.embedding`,
  `runbooks.embedding`) but nothing is embedded — that's Phase 8.
- Frontend is still a placeholder page, not a dashboard.
- No authentication — the `users` table exists only for remediation
  approval attribution later; there's no login flow.
