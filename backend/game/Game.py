import logging
from backend.game.deck.deck import Card, Deck

logger = logging.getLogger(__name__)

class GameState:
    def __init__(self, user_name: str, bet: int, balance: int = 1000):
        self.game_id = f"game_{user_name}_{id(self)}"
        self.user_name = user_name
        self.bet = bet
        self.player_balance = balance
        self.deck = Deck()
        self.player_cards = []
        self.dealer_cards = []
        self.game_state = "bet"  # bet, pTurn, dTurn, end
        self.result = None

    def card_to_dict(self, card: Card, hidden: bool = False):
        return {
            "value": card.rank,
            "suit": card.suit.lower(),
            "hidden": hidden
        }

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

    def start_game(self):
        self.player_cards = self.deck.deal(2)
        self.dealer_cards = self.deck.deal(2)
        self.game_state = "pTurn"

        logger.info(f"[{self.game_id}] [{self.user_name}] Game started with bet: {self.bet}")
        logger.info(f"[{self.game_id}] [{self.user_name}] Initial hand: {self.player_cards[0]}, {self.player_cards[1]} (value: {self.calculate_hand(self.player_cards)})")
        logger.info(f"[{self.game_id}] [Dealer] Initial hand: {self.dealer_cards[0]}, [hidden card]")

        if self.calculate_hand(self.player_cards) == 21:
            logger.info(f"[{self.game_id}] [{self.user_name}] BLACKJACK!")
            self.stand()

    def hit(self):
        if self.game_state != "pTurn":
            raise ValueError("Cannot hit - not player's turn")

        new_card = self.deck.deal_one()
        self.player_cards.append(new_card)
        hand_value = self.calculate_hand(self.player_cards)

        logger.info(f"[{self.game_id}] [{self.user_name}] Hit: drew {new_card}")
        logger.info(f"[{self.game_id}] [{self.user_name}] Current hand: {', '.join(str(c) for c in self.player_cards)} (value: {hand_value})")

        if hand_value > 21:
            logger.info(f"[{self.game_id}] [{self.user_name}] BUST! Dealer wins")
            self.game_state = "end"
            self.result = "dealer"
            self.player_balance -= self.bet

    def stand(self):
        if self.game_state != "pTurn":
            raise ValueError("Cannot stand - not player's turn")

        self.game_state = "dTurn"
        logger.info(f"[{self.game_id}] [{self.user_name}] Stand - player holds at {self.calculate_hand(self.player_cards)}")
        logger.info(f"[{self.game_id}] [Dealer] Revealed hand: {', '.join(str(c) for c in self.dealer_cards)} (value: {self.calculate_hand(self.dealer_cards)})")

        while self.calculate_hand(self.dealer_cards) < 17:
            new_card = self.deck.deal_one()
            self.dealer_cards.append(new_card)
            logger.info(f"[{self.game_id}] [Dealer] Hit: drew {new_card} (value: {self.calculate_hand(self.dealer_cards)})")

        player_value = self.calculate_hand(self.player_cards)
        dealer_value = self.calculate_hand(self.dealer_cards)

        self.game_state = "end"

        logger.info(f"[{self.game_id}] Game ended - Player: {player_value}, Dealer: {dealer_value}")

        if dealer_value > 21:
            logger.info(f"[{self.game_id}] [Dealer] BUST! Player wins")
            self.result = "player"
            self.player_balance += self.bet
        elif player_value > dealer_value:
            logger.info(f"[{self.game_id}] [{self.user_name}] Win")
            self.result = "player"
            self.player_balance += self.bet
        elif dealer_value > player_value:
            logger.info(f"[{self.game_id}] [Dealer] Win")
            self.result = "dealer"
            self.player_balance -= self.bet
        else:
            logger.info(f"[{self.game_id}] Draw")
            self.result = "draw"

        logger.info(f"[{self.game_id}] [{self.user_name}] New balance: {self.player_balance}")

    def to_response(self):
        data = {"gameState": self.game_state}

        if self.game_state == "bet":
            data["playerBalance"] = self.player_balance

        elif self.game_state in ("pTurn", "dTurn"):
            data["dealer"] = {
                "cards": [
                    self.card_to_dict(card, hidden=(i == 1 and self.game_state == "pTurn"))
                    for i, card in enumerate(self.dealer_cards)
                ]
            }
            data["player"] = {
                "cards": [self.card_to_dict(card) for card in self.player_cards]
            }

        elif self.game_state == "end":
            data["dealer"] = {
                "cards": [self.card_to_dict(card) for card in self.dealer_cards]
            }
            data["player"] = {
                "cards": [self.card_to_dict(card) for card in self.player_cards]
            }
            data["result"] = self.result
            data["playerBalance"] = self.player_balance

        return {"data": data}