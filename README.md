# TraceMind

**Agentic Software Reliability & Root-Cause Analysis Platform**

> TraceMind is an agentic software reliability platform that investigates
> software incidents by correlating operational evidence and generates
> evidence-backed root-cause hypotheses and validated remediation
> recommendations.

This is a portfolio project, built in phases, with a working deterministic
system underneath the AI layer — if you removed the LLM, the operational
data, dashboard, and evidence would still exist and be queryable.

**Status: Phase 2 of 15 — database schema (SQLAlchemy models + Alembic
migrations for all 15 tables).** No incident data, agents, or LLM calls
exist yet. See `docs/limitations.md` for an honest, continuously-updated
account of what is and isn't real — including which Phase 2 pieces are
not yet verified against a live database.

## Why this exists

Engineers investigating an incident normally dig manually through logs,
metrics, traces, recent deployments, past incidents, and runbooks.
TraceMind automates evidence collection and correlation, and clearly
separates observed facts, retrieved evidence, and AI-generated hypotheses
— it never presents an unverified hypothesis as a fact. Full problem
statement and design rationale: `docs/architecture.md`.

## Architecture (current target)

```
React frontend → FastAPI backend → { Incident Service, Investigation pipeline }
                                            │
                                   PostgreSQL + pgvector
                                            │
        Orchestrator → Evidence Collection → Evidence Correlation
              → Root Cause Analysis → Remediation → Validation
```

Full component diagram, data flow, schema, and agent responsibility
table: `docs/architecture.md` and the Phase 0 planning document.

## Tech stack

Python / FastAPI / Pydantic · React (Vite) · PostgreSQL + pgvector ·
LangGraph (from Phase 9) · Docker Compose · pytest

## Running it locally

```bash
cp .env.example .env
docker compose up --build
```

- Backend: http://localhost:8000 (OpenAPI docs at `/docs`)
- Frontend: http://localhost:5173
- Postgres: localhost:5432

Once containers are healthy, `http://localhost:5173` should show
"backend: ok, database: connected".

## Applying database migrations (Phase 2)

```bash
docker compose up -d db
cd backend
pip install -r requirements.txt
alembic upgrade head
```

This creates all 15 tables (services, logs, metrics, traces,
deployments, code_changes, historical_incidents, runbooks, incidents,
evidence, investigations, hypotheses, remediations, validation_runs)
and enables the pgvector extension. Verify with:

```bash
pytest tests/test_migrations.py -v
```

That test is skipped automatically if Postgres isn't reachable, so it
won't break a quick `pytest` run without the DB up — but it's the real
check that Phase 2 actually works, and it has not yet been run in this
project's development environment (no DB access there — see
`docs/limitations.md`). Run it before starting Phase 3.

## Running tests

```bash
# Backend (requires the db service running — docker compose up db)
cd backend
pip install -r requirements.txt
pytest tests -v

# Frontend
cd frontend
npm install
npm run test
```

## Repository structure

```
backend/     FastAPI app (api, models, schemas, services, agents, tools, evaluation)
frontend/    React dashboard + investigation workspace
simulator/   Simulated services + log/metric/trace/incident generators (Phase 3-5)
data/        Generated operational data + runbooks
docs/        architecture, agent-design, data-model, evaluation, security, limitations
scripts/     Utility scripts (e.g. generate_incidents.py)
```

## Project phases

| Phase | Scope | Status |
|---|---|---|
| 1 | Architecture + repo setup | ✅ |
| 2 | Database + schemas | ✅ this commit — **run migrations before Phase 3** (see below) |
| 3 | Simulated application | not started |
| 4 | Log/metric/trace generation | not started |
| 5 | Incident generator | not started |
| 6 | Frontend dashboard | not started |
| 7 | Deterministic investigation | not started |
| 8 | RAG | not started |
| 9 | Agent orchestration | not started |
| 10 | Root-cause analysis | not started |
| 11 | Remediation | not started |
| 12 | Sandbox validation | not started |
| 13 | Evaluation | not started |
| 14 | Testing + security | not started |
| 15 | Documentation + polish | not started |

## Documentation

- `docs/architecture.md` — components, data flow, agent graph
- `docs/agent-design.md` — per-agent responsibilities and tool contracts
- `docs/data-model.md` — database schema and indexing rationale
- `docs/evaluation.md` — benchmark methodology and results
- `docs/security.md` — current security posture
- `docs/limitations.md` — honest, continuously updated limitations
