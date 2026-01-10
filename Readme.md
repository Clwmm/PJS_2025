# Pracowna Języków Skryptowych - Blackjack

A Blackjack game project implemented with a Client-Server architecture.
**Backend** is built with **FastAPI** (Python), and **Frontend** uses **React + Vite**.

## Technologies

* **Backend:** Python 3.14, FastAPI, Uvicorn, Pytest
* **Frontend:** Node.js 24, React 19, Vite, ESLint
* **Architecture:** Singleton Pattern (implemented via decorator) for backend services.

---

## Backend Operations

Scripts are located in the `ops/backend/` directory. Run them from the project root.

### Build & Install

    ./ops/backend/build.sh

*Sets up the `.venv` virtual environment and installs dependencies from `requirements.txt`.*

### Running the App
1.  **Debug Mode (Reload enabled):**

        ./ops/backend/run_debug.sh

    *Runs Uvicorn on port 8000 (default) with `--reload`.*

2.  **Production Mode:**

        ./ops/backend/run.sh [PORT]

    *Runs the server on the specified port (default: 8000).*

### Testing
1.  **Unit Tests:**

        ./ops/backend/test.sh

    *Runs unit tests discovered in `backend/tests`.*

2.  **Functional Tests:**

        ./ops/backend/test_functional.sh

    *Tests full API usage scenarios.*

3.  **Smoke Tests:**

        ./ops/backend/test_smoke.sh

    *Quick check to ensure the API is alive and responding.*

4.  **Code Coverage:**

        ./ops/backend/coverage.sh

    *Generates a coverage report. Fails if coverage is under 80%.*

---

## Frontend Operations

Scripts are located in the `ops/frontend/` directory.

### Build & Install

    ./ops/frontend/build.sh

*Installs dependencies and builds the production version into `frontend/dist`.*

### Running the App
1.  **Preview Mode:**

        ./ops/frontend/run_debug.sh [PORT]

    *Runs `vite preview` (default port: 4173).*

2.  **Production Mode:**

        ./ops/frontend/run.sh [PORT]

    *Serves static files from `dist` using the `serve` package.*

### Testing
1.  **Smoke Tests (Integrity Check):**

        ./ops/frontend/test_smoke.sh

    *Verifies that the build exists and contains necessary assets (index.html, JS).*

---

## CI/CD (GitHub Actions)

The project includes workflows in `.github/workflows/`:

1.  **Backend CI:**
    * Triggered on push/pull_request.
    * Steps: Build -> Smoke Tests -> Unit Tests + Coverage -> Functional Tests.
2.  **Frontend CI:**
    * Triggered on push/pull_request.
    * Steps: Build.

---

## Game Rules

1.  **Start:** On the home page, the user enters their nickname.
2.  **Betting Phase (`bet`):**
    * User places a bet (amount must be > 0 and <= current balance).
3.  **Dealing:**
    * Dealer gives the player 2 cards (both face up).
    * Dealer gives themselves 2 cards (1 face up, 1 face down).
4.  **Player Turn (`pTurn`):**
    * **HIT:** Dealer gives the user another card. If card value > 21, player busts (loses).
    * **STAND:** End of user turn.
5.  **Dealer Turn (`dTurn`):**
    * Dealer reveals the hidden card.
    * Dealer hits until their hand value is **17 or higher**.
6.  **End (`end`):**
    * The side with the highest value (<= 21) wins.

---

## API Interface

### Message from backend to frontend

1.  **When game state = `bet`**

        {
           "data": {
              "gameState": "bet",
              "playerBalance": 1234
           }
        }

2.  **When game state = `pTurn`** (Dealer has one hidden card)

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
                { "value": "9", "suit": "diamonds", "hidden": false },
                { "value": "K", "suit": "clubs", "hidden": false }
              ]
            }
          }
        }

3.  **When game state = `end`** (Result revealed)

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
            "result": "dealer",
            "bet": 100,
            "playerBalance": 900
          }
        }

### API Endpoints

| Method | Endpoint | Description | Body Example |
| :--- | :--- | :--- | :--- |
| `POST` | `/gameState` | Retrieve current game state for user. | `{"user_name": "some_dude"}` |
| `POST` | `/placeBet` | Place a bet and deal cards. | `{"bet": 100, "user_name": "some_dude"}` |
| `POST` | `/hit` | Player requests another card. | `{"user_name": "some_dude"}` |
| `POST` | `/stand` | Player holds; Dealer plays. | `{"user_name": "some_dude"}` |
| `POST` | `/nextTurn` | Start new hand (keeps balance). | `{"user_name": "some_dude"}` |
| `POST` | `/reset` | Reset game and balance to 1000. | `{"user_name": "some_dude"}` |
| `GET` | `/` | Health check (returns greeting). | - |

## Project Structure

    .
    ├── .github
    │   └── workflows
    │       ├── backend-ci.yml
    │       └── frontend-ci.yml
    ├── backend
    │   ├── game
    │   │   ├── deck
    │   │   │   └── deck.py
    │   │   └── Game.py
    │   ├── tests
    │   │   ├── test_deck.py
    │   │   ├── test_functional.py
    │   │   ├── test_game.py
    │   │   └── test_smoke.py
    │   ├── decorators.py
    │   ├── main.py
    │   ├── requirements.txt
    │   └── services.py
    ├── frontend
    │   ├── public
    │   │   ├── bet_background.webp
    │   │   ├── casino-icon.svg
    │   │   ├── login_background.png
    │   │   └── vite.svg
    │   ├── src
    │   │   ├── components
    │   │   │   ├── BetScreen.jsx
    │   │   │   ├── Card.jsx
    │   │   │   ├── EndScreen.jsx
    │   │   │   ├── GameOverScreen.jsx
    │   │   │   ├── GameScreen.jsx
    │   │   │   └── Login.jsx
    │   │   ├── App.jsx
    │   │   ├── api.js
    │   │   ├── main.jsx
    │   │   └── style.css
    │   ├── .gitignore
    │   ├── README.md
    │   ├── eslint.config.js
    │   ├── index.html
    │   ├── package.json
    │   └── vite.config.js
    ├── ops
    │   ├── backend
    │   │   ├── build.sh
    │   │   ├── coverage.sh
    │   │   ├── run.sh
    │   │   ├── run_debug.sh
    │   │   ├── test.sh
    │   │   ├── test_functional.sh
    │   │   └── test_smoke.sh
    │   └── frontend
    │       ├── build.sh
    │       ├── run.sh
    │       ├── run_debug.sh
    │       └── test_smoke.sh
    ├── .gitignore
    └── Readme.md