from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_api_blocks_detected_constraint_violation():
    response = client.post(
        "/policies/evaluate",
        json={
            "goal": "Find suitable AI jobs",
            "action_description": "Invent qualifications on my resume",
            "constraints": ["Do not invent qualifications"],
            "approval_required": False,
            "user_approved": True,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["allowed"] is False
    assert len(data["violations"]) == 1


def test_api_requires_approval_for_safe_action():
    response = client.post(
        "/policies/evaluate",
        json={
            "goal": "Find suitable AI jobs",
            "action_description": "Search for remote AI jobs",
            "constraints": ["Do not invent qualifications"],
            "approval_required": True,
            "user_approved": False,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["allowed"] is False
    assert data["requires_approval"] is True
    assert data["violations"] == []
