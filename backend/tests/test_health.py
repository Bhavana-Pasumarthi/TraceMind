"""
Phase 1 exit-criteria test: the app boots and can prove DB connectivity.
Run with: pytest backend/tests -v
(requires the db service to be up — see README "Running tests")
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check_returns_ok():
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["database"] == "connected"
