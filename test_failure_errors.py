
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_missing_lesson_returns_404():
    response = client.post("/lessons/999999/verify")

    assert response.status_code == 404
    assert response.json()["detail"] == "Lesson not found"
