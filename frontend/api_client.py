import requests


API_BASE_URL = "http://127.0.0.1:8000"


def create_debate(
    topic: str,
    rounds: int,
) -> dict:

    response = requests.post(
        f"{API_BASE_URL}/api/debate",
        json={
            "topic": topic,
            "rounds": rounds,
        },
        timeout=300,
    )

    response.raise_for_status()

    return response.json()


def get_debates() -> list:

    response = requests.get(
        f"{API_BASE_URL}/api/debates",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_debate(
    debate_id: int,
) -> dict:

    response = requests.get(
        f"{API_BASE_URL}/api/debates/{debate_id}",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()

    