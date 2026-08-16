-- Runs automatically on first container start (docker-entrypoint-initdb.d).
-- Enables the pgvector extension used for runbook and historical-incident
-- embeddings (see docs/data-model.md, Phase 2).
CREATE EXTENSION IF NOT EXISTS vector;
