from fastapi.testclient import TestClient

from app.main import app


def test_home_page_responds():
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert "Gym Tracker" in response.text
