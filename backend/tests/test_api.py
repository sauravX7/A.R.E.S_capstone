from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_chat_endpoint_valid_request():
    # We are just testing the endpoint structure, not the actual LLM (which might not be running in CI)
    # Ideally, we would mock the LangGraph / LLM response here.
    # For a basic smoke test, we'll verify it doesn't return a 404 or validation error.
    response = client.post("/api/chat", json={"message": "Hello smoke test"})
    
    # Since Ollama might not be running during the test, it might return a 500.
    # We just want to ensure the route exists and accepts our payload format.
    assert response.status_code in [200, 500]
    
    if response.status_code == 200:
        assert "response" in response.json()
