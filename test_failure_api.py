
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_failure():
    response = client.post(
        "/failures",
        json={
            "action_description": "Recommend an onsite job",
            "failure_reason": "The user asked to prioritize remote jobs.",
            "expected_behavior": "Check location constraints before recommending a job.",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Failure recorded successfully"


def test_get_failures():
    response = client.get("/failures")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
