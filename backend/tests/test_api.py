from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "running"


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "healthy"


def test_invalid_rounds():

    response = client.post(
        "/api/debate",
        json={
            "topic": "Should AI replace software developers?",
            "rounds": 4,
        },
    )

    assert response.status_code == 400

def test_debate_not_found():

    response = client.get(
        "/api/debates/999999"
    )

    assert response.status_code == 404

    assert response.json()["detail"] == (
        "Debate not found."
    )

def test_list_debates():

    response = client.get(
        "/api/debates"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )