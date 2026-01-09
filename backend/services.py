import logging
from backend.decorators import singleton
from backend.game.deck.deck import Deck
from backend.game.Game import GameState

logger = logging.getLogger(__name__)


# --- SERVICE 1: ZARZĄDZANIE GRACZEM (SALDO) ---
@singleton
class PlayerService:
    def __init__(self):
        self._balances = {}

    def get_balance(self, user_name: str) -> int:
        if user_name not in self._balances:
            self._balances[user_name] = 1000
        return self._balances[user_name]

    def update_balance(self, user_name: str, amount: int):
        current = self.get_balance(user_name)
        self._balances[user_name] = current + amount

    def reset_balance(self, user_name: str):
        self._balances[user_name] = 1000


# --- SERVICE 2: ZASADY GRY (LOGIKA) ---
@singleton
class RulesService:
    def calculate_hand(self, cards):
        total = 0
        aces = 0
        for card in cards:
            if card.rank in ("J", "Q", "K"):
                total += 10
            elif card.rank == "A":
                total += 11
                aces += 1
            else:
                total += int(card.rank)

        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total

    def should_dealer_hit(self, dealer_hand_value):
        return dealer_hand_value < 17

    def determine_winner(self, player_value, dealer_value):
        if player_value > 21: return "dealer"
        if dealer_value > 21: return "player"
        if player_value > dealer_value: return "player"
        if dealer_value > player_value: return "dealer"
        return "draw"


# --- SERVICE 3: MENEDŻER GRY ---
@singleton
class GameService:
    def __init__(self):
        self.games = {}
        # Pobieramy instancje singletonów
        self.player_service = PlayerService.get_instance()
        self.rules_service = RulesService.get_instance()

    def get_game(self, user_name: str):
        return self.games.get(user_name)

    def create_game(self, user_name: str, bet: int):
        balance = self.player_service.get_balance(user_name)
        if bet > balance:
            raise ValueError("Insufficient balance")
        if bet <= 0:
            raise ValueError("Bet must be positive")

        self.player_service.update_balance(user_name, -bet)

        game = GameState(user_name, bet)
        game.player_cards = game.deck.deal(2)
        game.dealer_cards = game.deck.deal(2)
        game.game_state = "pTurn"

        if self.rules_service.calculate_hand(game.player_cards) == 21:
            logger.info(f"[{user_name}] Blackjack on start!")
            self._finalize_stand(game)

        self.games[user_name] = game
        return game

    def hit(self, user_name: str):
        game = self.get_game(user_name)
        if not game or game.game_state != "pTurn":
            raise ValueError("Cannot hit")

        new_card = game.deck.deal_one()
        game.player_cards.append(new_card)

        if self.rules_service.calculate_hand(game.player_cards) > 21:
            game.game_state = "end"
            game.result = "dealer"

        return game

    def stand(self, user_name: str):
        game = self.get_game(user_name)
        if not game or game.game_state != "pTurn":
            raise ValueError("Cannot stand")

        game.game_state = "dTurn"
        self._finalize_stand(game)
        return game

    def _finalize_stand(self, game: GameState):
        dealer_val = self.rules_service.calculate_hand(game.dealer_cards)
        while self.rules_service.should_dealer_hit(dealer_val):
            game.dealer_cards.append(game.deck.deal_one())
            dealer_val = self.rules_service.calculate_hand(game.dealer_cards)

        player_val = self.rules_service.calculate_hand(game.player_cards)
        result = self.rules_service.determine_winner(player_val, dealer_val)

        game.game_state = "end"
        game.result = result

        if result == "player":
            self.player_service.update_balance(game.user_name, game.bet * 2)
        elif result == "draw":
            self.player_service.update_balance(game.user_name, game.bet)

    def next_turn(self, user_name: str):
        if user_name in self.games:
            del self.games[user_name]
        return {
            "gameState": "bet",
            "playerBalance": self.player_service.get_balance(user_name)
        }

    def reset_game(self, user_name: str):
        if user_name in self.games:
            del self.games[user_name]
        self.player_service.reset_balance(user_name)
        return {
            "gameState": "bet",
            "playerBalance": 1000
        }

    def get_formatted_state(self, user_name: str):
        balance = self.player_service.get_balance(user_name)
        game = self.get_game(user_name)
        if not game:
            return {"data": {"gameState": "bet", "playerBalance": balance}}
        return game.to_response(balance)