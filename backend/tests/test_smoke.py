from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_api_is_alive():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI Blackjack (Decorator Pattern)!!!"}

def test_critical_game_initialization():
    username = "smoke_tester"
    
    response = client.post("/gameState", json={"user_name": username})
    
    assert response.status_code == 200
    data = response.json()["data"]
    
    assert "gameState" in data
    assert "playerBalance" in data
    assert data["gameState"] == "bet"
