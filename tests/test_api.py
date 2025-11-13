"""API endpoint tests."""
import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns expected response."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data


# TODO: Add tests for OCR endpoint
# TODO: Add tests for extraction endpoint
# TODO: Add tests for file upload endpoint
# TODO: Add integration tests with mock API responses
