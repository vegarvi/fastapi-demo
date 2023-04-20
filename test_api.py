"""Unit tests for FastAPI Hello World and trying to push to main"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    """Tests function to check the response and message"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
