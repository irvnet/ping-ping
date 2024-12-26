from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Ping-Pong App is Running"}

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "Ping-Ping is Healthy"}
