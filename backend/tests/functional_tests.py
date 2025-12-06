from fastapi.testclient import TestClient
from backend.main import app, games

client = TestClient(app)

def reset_user(username: str):
    if username in games:
        del games[username]

def test_bet_value_over_balance():
    username = "bad_bet_user"
    reset_user(username)

    response = client.post("/placeBet", json={
        "user_name": username,
        "bet": 5000
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient balance"

    response = client.post("/placeBet", json={
        "user_name": username,
        "bet": -10
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Bet must be positive"
