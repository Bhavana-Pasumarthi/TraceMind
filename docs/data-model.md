# Data Model

Not yet implemented — the real schema (SQLAlchemy models + Alembic
migrations) lands in Phase 2. The pgvector extension is already enabled
(`backend/app/database/init/001_extensions.sql`) so Phase 2 can go
straight to defining tables and embedding columns.

See the Phase 0 plan for the target schema (`historical_incidents`,
`runbooks`, `logs`, `metrics`, `traces`, `deployments`, `code_changes`,
`incidents`, `evidence`, `investigations`, `hypotheses`, `remediations`,
`validation_runs`) — this file will be rewritten to describe what's
actually built once Phase 2 lands, including the real indexing choices
and any deviations from the original plan.
