from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<h1>Welcome to the Ping-Pong App!</h1>" in response.text
    assert "<p>The app is up and running!</p>" in response.text

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "Ping-Ping is Healthy"}
