# Pracownia Języków Skryptowych 2025

## BACKEND
1. Build
```./opt/backend/build.sh```
2. Run
```./opt/backend/run.sh```

## FRONTEND



## Game States
At home page user puts his nickname. 
1. Place a bet
   * User places a bet with a selected number of money
2. After placing bet Dealer gives player 2 card (face up) and gives
himself 2 cards (1 face up, 1 face down)
3. Now user have 2 choices:
   * HIT: Dealer give user another card
   * STAND: End of user turn
4. After player choose STAND, dealer play solo
5. Player with the highest value of cards wins (when the value is less or equal to 21)

## Interface

### Game will have 4 states:
   * bet
   * pTurn
   * dTurn
   * end

### Message from backend to frontend

1. When game state = bet

```json
{
   "data": {
      "gameState": "bet",
      "playerBalance": 1234
   }
}
```

2. When game state = pTurn || dTurn

```json
{
  "data": {
    "gameState": "pTurn",
    "dealer": {
      "cards": [
        { "value": "10", "suit": "hearts", "hidden": false },
        { "value": "K", "suit": "spades", "hidden": true }
      ]
    },
    "player": {
      "cards": [
        { "value": "9", "suit": "diamonds" },
        { "value": "K", "suit": "clubs" }
      ]
    }
  }
}
```

3. When game state = end

```json
{
  "data": {
    "gameState": "end",
    "dealer": {
      "cards": [
        { "value": "10", "suit": "hearts" },
        { "value": "A", "suit": "spades" }
      ]
    },
    "player": {
      "cards": [
        { "value": "9", "suit": "diamonds" },
        { "value": "K", "suit": "clubs" }
      ]
    },
    "result": "dealer"
  }
}
```

### Api endpoints

1. POST /placeBet <br>
body:
```json
{
   "bet": 100,
   "user_name": "some_dude_1923"
}
```
2. POST /hit <br>
body:
```json
{
   "user_name": "some_dude_1923"
}
```
3. POST /stand <br>
body:
```json
{
   "user_name": "some_dude_1923"
}
```
4. POST /nextTurn <br>
body:
```json
{
   "user_name": "some_dude_1923"
}
```
5. GET /gameState <br>
body:
```json
{
   "user_name": "some_dude_1923"
}
```