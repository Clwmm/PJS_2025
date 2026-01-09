from fastapi.testclient import TestClient
from backend.main import app
from backend.services import GameService

client = TestClient(app)
game_service = GameService.get_instance()


def reset_user(username: str):
    if username in game_service.games:
        del game_service.games[username]
    game_service.player_service.reset_balance(username)


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


# PLACE BESTS - /placeBet
def test_place_bet_valid():
    username = "valid_bet_user"
    reset_user(username)

    response = client.post("/placeBet", json={"user_name": username, "bet": 100})
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["gameState"] in ["pTurn", "end"]
    assert len(data["player"]["cards"]) == 2


def test_bet_value_over_balance():
    username = "bad_bet_user"
    reset_user(username)
    response = client.post("/placeBet", json={"user_name": username, "bet": 5000})
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient balance"


def test_bet_negative_value():
    username = "negative_bet_user"
    reset_user(username)
    response = client.post("/placeBet", json={"user_name": username, "bet": -10})
    assert response.status_code == 400


def test_bet_zero_value():
    username = "zero_bet_user"
    reset_user(username)
    response = client.post("/placeBet", json={"user_name": username, "bet": 0})
    assert response.status_code == 400


# HIT TESTS -> /hit
def test_hit_valid():
    username = "hit_user"
    reset_user(username)
    client.post("/placeBet", json={"user_name": username, "bet": 50})

    game = game_service.get_game(username)
    if game.game_state == "pTurn":
        initial_count = len(game.player_cards)
        response = client.post("/hit", json={"user_name": username})
        assert response.status_code == 200
        assert len(response.json()["data"]["player"]["cards"]) == initial_count + 1


def test_hit_no_game():
    username = "no_game_user"
    reset_user(username)

    response = client.post("/hit", json={"user_name": username})
    # Zmiana: oczekujemy 400, bo GameService rzuca ValueError("Cannot hit")
    assert response.status_code == 400
    assert "Cannot hit" in response.json()["detail"]


def test_hit_after_stand():
    username = "hit_after_stand_user"
    reset_user(username)
    client.post("/placeBet", json={"user_name": username, "bet": 50})

    game = game_service.get_game(username)
    if game.game_state == "pTurn":
        client.post("/stand", json={"user_name": username})
        response = client.post("/hit", json={"user_name": username})
        assert response.status_code == 400


def test_hit_multiple_times():
    username = "multi_hit_user"
    reset_user(username)
    client.post("/placeBet", json={"user_name": username, "bet": 50})

    game = game_service.get_game(username)
    hit_count = 0
    while game.game_state == "pTurn" and hit_count < 5:
        response = client.post("/hit", json={"user_name": username})
        assert response.status_code == 200
        hit_count += 1
        if game.game_state == "end": break
    assert hit_count >= 1


# STAND TESTS -> /stand
def test_stand_valid():
    username = "stand_user"
    reset_user(username)
    client.post("/placeBet", json={"user_name": username, "bet": 50})

    game = game_service.get_game(username)
    if game.game_state == "pTurn":
        response = client.post("/stand", json={"user_name": username})
        assert response.status_code == 200
        assert response.json()["data"]["gameState"] == "end"


def test_stand_changes_state_to_end():
    username = "stand_logic_user"
    reset_user(username)

    client.post("/placeBet", json={"user_name": username, "bet": 100})

    response = client.post("/gameState", json={"user_name": username})
    current_state = response.json()["data"]["gameState"]

    if current_state == "pTurn":
        response = client.post("/stand", json={"user_name": username})
        assert response.status_code == 200
        data = response.json()["data"]

        assert data["gameState"] == "end"
        assert "result" in data

        assert data["dealer"]["cards"][1]["hidden"] is False


def test_stand_when_not_turn():
    """Próba wykonania stand, gdy gra się jeszcze nie zaczęła"""
    username = "premature_stand_user"
    reset_user(username)

    response = client.post("/stand", json={"user_name": username})
    assert response.status_code == 400


# NEXT TURN TESTS -> /nextTurn

def test_next_turn_resets_game_state():
    username = "next_turn_user"
    reset_user(username)

    client.post("/placeBet", json={"user_name": username, "bet": 100})

    response = client.post("/nextTurn", json={"user_name": username})
    assert response.status_code == 200
    data = response.json()["data"]

    assert data["gameState"] == "bet"
    assert isinstance(data["playerBalance"], int)


def test_next_turn_preserves_balance():
    username = "balance_keeper"
    reset_user(username)

    client.post("/placeBet", json={"user_name": username, "bet": 100})

    response = client.post("/nextTurn", json={"user_name": username})
    data = response.json()["data"]

    assert data["playerBalance"] == 900


# RESET TESTS -> /reset

def test_reset_restores_balance():
    username = "reset_test_user"
    reset_user(username)

    client.post("/placeBet", json={"user_name": username, "bet": 500})

    response = client.post("/reset", json={"user_name": username})
    assert response.status_code == 200
    data = response.json()["data"]

    assert data["gameState"] == "bet"
    assert data["playerBalance"] == 1000


# WHOLE FLOW TEST

def test_full_game_flow():
    """
    Symulacja pełnego cyklu życia gracza:
    1. Wejście do gry
    2. Postawienie zakładu
    3. Dobranie karty (Hit)
    4. Pasowanie (Stand)
    5. Sprawdzenie wyniku
    6. Nowa tura
    """
    username = "flow_master"
    reset_user(username)

    r1 = client.post("/gameState", json={"user_name": username})
    assert r1.json()["data"]["gameState"] == "bet"
    initial_balance = r1.json()["data"]["playerBalance"]

    bet_amount = 200
    r2 = client.post("/placeBet", json={"user_name": username, "bet": bet_amount})
    assert r2.status_code == 200
    state_after_bet = r2.json()["data"]["gameState"]

    if state_after_bet == "pTurn":
        r3 = client.post("/hit", json={"user_name": username})
        assert r3.status_code == 200
        state_after_hit = r3.json()["data"]["gameState"]

        if state_after_hit == "pTurn":
            r4 = client.post("/stand", json={"user_name": username})
            assert r4.status_code == 200
            final_data = r4.json()["data"]
            assert final_data["gameState"] == "end"
            assert final_data["result"] in ["player", "dealer", "draw"]
        else:
            assert state_after_hit == "end"
            assert r3.json()["data"]["result"] == "dealer"

    elif state_after_bet == "end":
        assert r2.json()["data"]["result"] == "player"

    r5 = client.post("/nextTurn", json={"user_name": username})
    assert r5.status_code == 200
    new_game_data = r5.json()["data"]

    assert new_game_data["gameState"] == "bet"
    assert new_game_data["playerBalance"] is not None