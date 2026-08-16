"""
Health check endpoint.

Deliberately checks a real DB round-trip (not just "is the process up")
so that Phase 1's exit criteria — "docker compose up boots empty
services" — actually proves the backend can talk to Postgres, which
every later phase depends on.
"""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.session import get_db

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check(db: Session = Depends(get_db)) -> dict:
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}
