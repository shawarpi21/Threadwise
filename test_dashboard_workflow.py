from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_dashboard_can_create_goal():
    response = client.post(
        "/goals",
        json={
            "goal": "Provide reliable answers",
            "constraints": ["Do not invent facts"],
            "approval_required": True,
        },
    )

    assert response.status_code in (200, 201)

    data = response.json()

    # The API returns the saved goal inside a "goal" object.
    saved_goal = data["goal"]

    assert saved_goal["goal"] == "Provide reliable answers"
    assert saved_goal["constraints"] == ["Do not invent facts"]
    assert saved_goal["approval_required"] is True


def test_dashboard_can_record_failure():
    response = client.post(
        "/failures",
        json={
            "action_description": "Agent gave wrong answer",
            "failure_reason": "The answer lacked evidence",
            "expected_behavior": "Check evidence before answering",
        },
    )

    assert response.status_code in (200, 201)

    data = response.json()

    assert data["action_description"] == "Agent gave wrong answer"
    assert data["failure_reason"] == "The answer lacked evidence"
    assert (
        data["expected_behavior"]
        == "Check evidence before answering"
    )
