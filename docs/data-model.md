# Data Model

Implemented as of Phase 2. SQLAlchemy 2.0-style declarative models live
in `backend/app/models/`, one file per table; `backend/app/models/enums.py`
holds shared enums (log level, severity, incident status, evidence
category, etc.) so the same allowed values are enforced everywhere,
including later in agent/tool code.

## Tables

| Table | Purpose | Key relationships |
|---|---|---|
| `services` | Reference table for the 4 simulated services | referenced by almost everything below |
| `users` | Minimal identity, for remediation approval attribution | `remediations.approved_by` |
| `logs` | Application log lines | `service_id` FK; indexed on `(service_id, timestamp)` |
| `metrics` | Per-service numeric samples over time | `service_id` FK; indexed on `(service_id, timestamp)` |
| `traces` | Spans across a request chain | grouped by `trace_id`; indexed on `(service_id, start_time)` |
| `deployments` | Deploys of a service | `service_id` FK |
| `code_changes` | File-level change metadata | `service_id` FK, optional `deployment_id` FK |
| `historical_incidents` | RAG target: past incidents | `embedding vector(1536)`, nullable until Phase 8 |
| `runbooks` | RAG target: troubleshooting docs | `embedding vector(1536)`, nullable until Phase 8 |
| `incidents` | Central row a user investigates | `scenario_id` — ground truth pointer, never read by the agent pipeline |
| `evidence` | Every FACT/EVIDENCE item collected | FKs to `incidents`, `investigations`; `source_type`+`source_ref_id` point at the origin row |
| `investigations` | One row per "Investigate" run | FK to `incidents`; `plan_json` from the Orchestrator |
| `hypotheses` | Ranked root-cause candidates | `supporting_evidence_ids`/`contradicting_evidence_ids` are Postgres arrays of `evidence.id` |
| `remediations` | Proposed fixed-catalog actions | FK to `hypotheses`; `approved_by`/`approved_at` = human-in-the-loop audit trail |
| `validation_runs` | Sandbox validation outcomes | FK to `remediations`; structured `tests_run_json`/`results_json` |

## Design decisions worth defending

- **Metrics are fixed numeric columns, not an EAV/key-value table.**
  Anomaly detection (Phase 9) needs real arithmetic on these values;
  a generic key-value schema would make that slow and awkward. The
  tradeoff is that adding a new metric type later means a migration —
  acceptable at this project's scope.
- **One Postgres instance with pgvector, not a separate vector DB.**
  Embedding volume (runbooks + historical incidents) is small; this
  avoids an extra service to run/explain while still demonstrating
  real vector retrieval. See `docs/architecture.md` / the Phase 0 plan
  for the fuller comparison.
- **`evidence.payload_json` denormalizes a snapshot of the source row**
  at collection time, rather than requiring a join back to `logs`/
  `metrics`/etc. every time an investigation is rendered. This trades a
  bit of duplication for simpler, faster reads on the (very common)
  "show me this investigation" path.
- **`hypotheses.confidence` is explicitly system/model confidence, not
  ground truth** — enforced by keeping ground truth (`incidents.scenario_id`
  → failure scenario spec) in a path the agent pipeline never queries.
- **Enums are enforced at the schema level** (Postgres `ENUM` types via
  SQLAlchemy `Enum`), including `evidence.category` (`fact`/`evidence`)
  — the FACT vs. EVIDENCE distinction is a database constraint, not
  just a convention in prompt text.

## Migrations

Alembic is configured in `backend/alembic.ini` / `backend/migrations/`.
`migrations/env.py` reads `DATABASE_URL` from `app.config.get_settings()`
(the same source the app uses) rather than duplicating it, so migrations
can't silently drift from the app's actual DB config.

`migrations/versions/0001_initial_schema.py` creates all 15 tables. It
was **hand-written to mirror `app/models/*.py`** rather than produced by
`alembic revision --autogenerate`, because this development sandbox has
no network access to run migrations against a live Postgres. Before
Phase 3 starts, run it for real:

```bash
docker compose up -d db
cd backend
alembic upgrade head
pytest tests/test_migrations.py -v   # applies + verifies against the real DB
```

From Phase 3 onward, prefer `alembic revision --autogenerate -m "..."`
for any further schema changes — 0001 is the one exception, not the
established workflow.
