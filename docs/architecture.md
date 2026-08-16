# Architecture

See the full Phase 0 architecture & planning document for the component
diagram, data flow, database schema, and agent responsibility table:
`tracemind-architecture-plan.md` (kept alongside this repo during
development; contents will be folded into this file as the system is
actually built, so this doc always reflects what's *really implemented*
rather than what's planned).

## Current status (Phase 1)

- Repo scaffold, Docker Compose (Postgres + backend + frontend), and a
  health-check endpoint proving frontend → backend → Postgres connectivity.
- No incident data, no agents, no LLM calls yet — those arrive in later
  phases per the plan.

## Agent graph (as of the Phase 0 revision)

```
Orchestrator
     ↓
Evidence Collection   (tools: logs, metrics, traces, deployments — no LLM)
     ↓
Evidence Correlation
     ↓
Root Cause Analysis
     ↓
Remediation
     ↓
Validation
```

Evidence Collection is a single stage that calls four deterministic tool
functions rather than four separate autonomous agents — see the project
history for the reasoning (fewer unnecessary LLM calls, matches the
"prefer deterministic logic where sufficient" principle, still fully
explainable). This stage is not implemented until Phase 9; Phases 1-8
build the deterministic system and RAG pipeline first.
