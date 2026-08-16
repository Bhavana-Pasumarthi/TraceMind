"""
TraceMind backend entrypoint.

Phase 1 scope: app boots, serves OpenAPI docs, and proves DB connectivity
via /api/health. Incident/investigation routers are added starting Phase 2.
"""

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health
from app.config import get_settings

settings = get_settings()
logger = structlog.get_logger()

app = FastAPI(
    title="TraceMind API",
    description=(
        "Agentic software reliability & root-cause analysis platform — "
        "backend API. See /docs for the interactive OpenAPI schema."
    ),
    version="0.1.0",
)

# Permissive in dev; tighten before anything resembling a real deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.environment == "development" else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")


@app.on_event("startup")
def on_startup() -> None:
    logger.info("tracemind_backend_starting", environment=settings.environment)
