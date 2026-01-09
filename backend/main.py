from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import logging

from backend.services import GameService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('blackjack.log')]
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ZMIANA: Pobranie instancji przez get_instance()
game_service = GameService.get_instance()

class PlaceBetRequest(BaseModel):
    bet: int
    user_name: str

class UserRequest(BaseModel):
    user_name: str

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI Blackjack (Decorator Pattern)!!!"}

@app.post("/gameState")
def get_game_state(request: UserRequest):
    return game_service.get_formatted_state(request.user_name)

@app.post("/placeBet")
def place_bet(request: PlaceBetRequest):
    try:
        game_service.create_game(request.user_name, request.bet)
        return game_service.get_formatted_state(request.user_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/hit")
def hit(request: UserRequest):
    try:
        game_service.hit(request.user_name)
        return game_service.get_formatted_state(request.user_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/stand")
def stand(request: UserRequest):
    try:
        game_service.stand(request.user_name)
        return game_service.get_formatted_state(request.user_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/nextTurn")
def next_turn(request: UserRequest):
    data = game_service.next_turn(request.user_name)
    return {"data": data}

@app.post("/reset")
def reset(request: UserRequest):
    data = game_service.reset_game(request.user_name)
    return {"data": data}