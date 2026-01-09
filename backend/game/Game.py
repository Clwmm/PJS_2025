from backend.game.deck.deck import Card, Deck

class GameState:
    def __init__(self, user_name: str, bet: int):
        self.user_name = user_name
        self.bet = bet
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

    # ZMIANA: Dodano argument current_balance
    def to_response(self, current_balance: int):
        data = {"gameState": self.game_state}

        if self.game_state == "bet":
            data["playerBalance"] = current_balance

        elif self.game_state in ("pTurn", "dTurn"):
            # Karta dealera ukryta tylko w turze gracza i tylko druga karta
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
            data["bet"] = self.bet
            data["playerBalance"] = current_balance

        return {"data": data}