
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_create_lesson():
    response = client.post(
        "/lessons",
        json={
            "title": "Check job location",
            "description": "Compare job location with user preferences.",
            "evidence": (
                "A test showed an onsite-only job "
                "violated the remote preference."
            ),
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Lesson saved successfully"
    assert data["id"] is not None
    assert data["verified"] is False

def test_verify_lesson_rejects_evidence_same_as_description():
    response = client.post(
        "/lessons",
        json={
            "title": "Reliable memory lesson",
            "description": "Evidence should support the lesson clearly.",
            "evidence": "Evidence should support the lesson clearly.",
        },
    )

    assert response.status_code in (200, 201)
    lesson_id = response.json()["id"]

    verify_response = client.post(
        f"/lessons/{lesson_id}/verify"
    )

    assert verify_response.status_code == 400
    assert (
        verify_response.json()["detail"]
        == "Evidence must be different from the lesson description."
    )


def test_verify_lesson_returns_404_for_missing_lesson():
    response = client.post("/lessons/999999/verify")

    assert response.status_code == 404
    assert response.json()["detail"] == "Lesson not found"
