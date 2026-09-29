from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_qna():
    response = client.get("/api/qna", params={"question": "What is Python?"})
    assert response.status_code == 200
    assert response.json()["answer"]


def test_explain():
    response = client.post("/api/explain", json={"topic": "photosynthesis"})
    assert response.status_code == 200
    assert response.json()["topic"] == "photosynthesis"
    assert response.json()["explanation"]


def test_summarize():
    response = client.post(
        "/api/summarize",
        json={"text": "Photosynthesis converts light energy into chemical energy."},
    )
    assert response.status_code == 200
    assert response.json()["summary"]


def test_quiz():
    response = client.post(
        "/api/quiz",
        json={"text": "The Earth orbits the Sun."},
    )
    assert response.status_code == 200
    quiz = response.json()["quiz"]
    assert len(quiz) >= 3
    assert all(len(item["options"]) == 4 for item in quiz)
    assert all(item["answer"] in item["options"] for item in quiz)


def test_learning_path():
    response = client.get(
        "/api/learn/recommendations",
        params={"topic": "SQL"},
    )
    assert response.status_code == 200
    assert response.json()["topic"] == "SQL"
    assert response.json()["recommendation"]


def test_validation():
    response = client.post("/api/explain", json={"topic": ""})
    assert response.status_code == 422
