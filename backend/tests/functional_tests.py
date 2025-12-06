from fastapi.testclient import TestClient
from backend.main import app, games

client = TestClient(app)

def reset_user(username: str):
    if username in games:
        del games[username]

# USER TESTS -> /gameState
def test_get_game_state_new_user():
    username = "new_user"
    reset_user(username)

    response = client.post("/gameState", json={"user_name": username})
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["gameState"] == "bet"
    assert data["playerBalance"] == 1000


def test_get_game_state_existing_user():
    username = "existing_user"
    reset_user(username)

    client.post("/placeBet", json={"user_name": username, "bet": 50})

    response = client.post("/gameState", json={"user_name": username})
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["gameState"] in ["pTurn", "end"]
    assert "player" in data
    assert "dealer" in data

# PLACE BESTS - /placeBet
def test_place_bet_valid():
    username = "valid_bet_user"
    reset_user(username)

    response = client.post("/placeBet", json={
        "user_name": username,
        "bet": 100
    })
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["gameState"] in ["pTurn", "end"]  # end if 21
    assert "player" in data
    assert "dealer" in data
    assert len(data["player"]["cards"]) == 2
    assert len(data["dealer"]["cards"]) == 2


def test_bet_value_over_balance():
    """Test that betting more than available balance is rejected"""
    username = "bad_bet_user"
    reset_user(username)

    response = client.post("/placeBet", json={
        "user_name": username,
        "bet": 5000
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient balance"


def test_bet_negative_value():
    username = "negative_bet_user"
    reset_user(username)

    response = client.post("/placeBet", json={
        "user_name": username,
        "bet": -10
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Bet must be positive"


def test_bet_zero_value():
    username = "zero_bet_user"
    reset_user(username)

    response = client.post("/placeBet", json={
        "user_name": username,
        "bet": 0
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Bet must be positive"

#todo: testy bet

# HIT TESTS -> /hit
def test_hit_valid():
    username = "hit_user"
    reset_user(username)

    client.post("/placeBet", json={
        "user_name": username,
        "bet": 50
    })

    game = games[username]
    if game.game_state == "pTurn":
        initial_card_count = len(game.player_cards)

        response = client.post("/hit", json={"user_name": username})
        assert response.status_code == 200
        data = response.json()["data"]

        assert len(data["player"]["cards"]) == initial_card_count + 1


def test_hit_no_game():
    username = "no_game_user"
    reset_user(username)

    response = client.post("/hit", json={"user_name": username})
    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found"

def test_hit_after_stand():
    username = "hit_after_stand_user"
    reset_user(username)

    client.post("/placeBet", json={"user_name": username, "bet": 50})

    game = games[username]
    if game.game_state == "pTurn":
        client.post("/stand", json={"user_name": username})

        response = client.post("/hit", json={"user_name": username})
        assert response.status_code == 400
        assert "not player's turn" in response.json()["detail"]


def test_hit_multiple_times():
    username = "multi_hit_user"
    reset_user(username)

    client.post("/placeBet", json={"user_name": username, "bet": 50})

    game = games[username]

    hit_count = 0
    while game.game_state == "pTurn" and hit_count < 5:
        response = client.post("/hit", json={"user_name": username})
        assert response.status_code == 200
        hit_count += 1

        if game.game_state == "end":
            break

    assert hit_count >= 1


# STAND TESTS -> /stand
def test_stand_valid():
    username = "stand_user"
    reset_user(username)

    client.post("/placeBet", json={
        "user_name": username,
        "bet": 50
    })

    response = client.post("/stand", json={"user_name": username})

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["gameState"] in ["end"]
    assert "player" in data
    assert "dealer" in data
    assert len(data["player"]["cards"]) >= 2
    assert len(data["dealer"]["cards"]) >= 2

#todo: STAND, NEXT TURN, RESET AND WHOLE FLOW TESTS




