from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.game.deck.deck import Deck, Card
from backend.game.Game import GameState

app = FastAPI()
games = {}


class PlaceBetRequest(BaseModel):
    bet: int
    user_name: str


class UserRequest(BaseModel):
    user_name: str


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI Blackjack!"}


@app.get("/gameState")
def get_game_state(user_name: str):
    """Pobierz stan gry dla danego użytkownika"""
    if user_name not in games:
        return {
            "data": {
                "gameState": "bet",
                "playerBalance": 1000  # domyślny balans
            }
        }
    return games[user_name].to_response()


@app.post("/placeBet")
def place_bet(request: PlaceBetRequest):
    """Postaw zakład i rozpocznij nową grę"""
    user_name = request.user_name
    bet = request.bet

    current_balance = 1000
    if user_name in games:
        current_balance = games[user_name].player_balance

    if bet > current_balance:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    if bet <= 0:
        raise HTTPException(status_code=400, detail="Bet must be positive")

    games[user_name] = GameState(user_name, bet, current_balance)
    games[user_name].start_game()

    return games[user_name].to_response()


@app.post("/hit")
def hit(request: UserRequest):
    """Gracz dobiera kartę"""
    user_name = request.user_name

    if user_name not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = games[user_name]

    try:
        game.hit()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return game.to_response()


@app.post("/stand")
def stand(request: UserRequest):
    """Gracz kończy turę - dealer gra"""
    user_name = request.user_name

    if user_name not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = games[user_name]

    try:
        game.stand()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return game.to_response()


@app.post("/nextTurn")
def next_turn(request: UserRequest):
    """Rozpocznij kolejną rundę (po zakończeniu gry)"""
    user_name = request.user_name

    if user_name not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = games[user_name]

    if game.game_state != "end":
        raise HTTPException(status_code=400, detail="Current game not finished")

    game.game_state = "bet"
    game.result = None
    game.player_cards = []
    game.dealer_cards = []
    game.deck = Deck()

    return game.to_response()
