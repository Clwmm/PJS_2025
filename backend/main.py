from fastapi import FastAPI
app = FastAPI()

games = {}

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "query": q}


@app.get("/gameState?user={userName}")
def get_game_state(user_name: str):
    if user_name not in games:
        return {
            "data" : {
                "gameState": "bet",
                "playerBalance": 1000 # domyślny balans
            }
        }
    return games[user_name].to_response()

@app.post("/placeBet")
def placeBets():
    return ''

@app.post("/hit")
def hit():
    return ''

@app.post("/stand")
def standBets():
    return ''

@app.post("/nextTurn")
def nextTurn():
    return ''


