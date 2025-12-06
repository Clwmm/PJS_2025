from backend.game.deck.deck import Card, Deck

class GameState:
    def __init__(self, user_name: str, bet: int, balance: int = 1000):
        self.user_name = user_name
        self.bet = bet
        self.player_balance = balance
        self.deck = Deck()
        self.player_cards = []
        self.dealer_cards = []
        self.game_state = "bet"  # bet, pTurn, dTurn, end
        self.result = None  # player, dealer, draw

    def card_to_dict(self, card: Card, hidden: bool = False):
        """Konwertuje kartę na dict zgodnie z formatem API"""
        return {
            "value": card.rank,
            "suit": card.suit.lower(),
            "hidden": hidden
        }

    def calculate_hand(self, cards):
        """Oblicza wartość ręki"""
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

        while total > 21 and aces > 0: # as to 1 jeśli gracz przekroczy 21
            total -= 10
            aces -= 1

        return total

    def start_game(self):
        """Rozpocznij grę - rozdaj karty"""
        self.player_cards = self.deck.deal(2)
        self.dealer_cards = self.deck.deal(2)
        self.game_state = "pTurn"

        print(f"Gra rozpoczęta! Stawka: {self.bet}")
        print(
            f"Gracz: {self.player_cards[0]}, {self.player_cards[1]} (wartość: {self.calculate_hand(self.player_cards)})")
        print(f"Dealer: {self.dealer_cards[0]}, [ukryta karta]")

        # Sprawdź blackjacka gracza
        if self.calculate_hand(self.player_cards) == 21:
            print("🎉 BLACKJACK!")
            self.stand()

    def hit(self):
        """Gracz bierze kartę"""
        if self.game_state != "pTurn":
            raise ValueError("Cannot hit - not player's turn")

        new_card = self.deck.deal_one()
        self.player_cards.append(new_card)
        hand_value = self.calculate_hand(self.player_cards)

        print(f"\n📥 Dobrano kartę: {new_card}")
        print(f"Ręka gracza: {', '.join(str(c) for c in self.player_cards)} (wartość: {hand_value})")

        if hand_value > 21:
            print("💥 PRZEBICIE! Dealer wygrywa!")
            self.game_state = "end"
            self.result = "dealer"
            self.player_balance -= self.bet

    def stand(self):
        """Gracz kończy turę, dealer gra"""
        if self.game_state != "pTurn":
            raise ValueError("Cannot stand - not player's turn")

        self.game_state = "dTurn"
        print(
            f"\n✋ Gracz pas! Ręka dealera: {', '.join(str(c) for c in self.dealer_cards)} (wartość: {self.calculate_hand(self.dealer_cards)})")

        # Dealer dobiera do 17
        while self.calculate_hand(self.dealer_cards) < 17:
            new_card = self.deck.deal_one()
            self.dealer_cards.append(new_card)
            print(f"Dealer dobiera: {new_card} (wartość: {self.calculate_hand(self.dealer_cards)})")

        # Ustal wynik
        player_value = self.calculate_hand(self.player_cards)
        dealer_value = self.calculate_hand(self.dealer_cards)

        self.game_state = "end"

        print(f"\n📊 Wynik końcowy:")
        print(f"Gracz: {player_value}")
        print(f"Dealer: {dealer_value}")

        if dealer_value > 21:
            print("🎉 Dealer przebił! Gracz wygrywa!")
            self.result = "player"
            self.player_balance += self.bet
        elif player_value > dealer_value:
            print("🎉 Gracz wygrywa!")
            self.result = "player"
            self.player_balance += self.bet
        elif dealer_value > player_value:
            print("😞 Dealer wygrywa!")
            self.result = "dealer"
            self.player_balance -= self.bet
        else:
            print("🤝 Remis!")
            self.result = "draw"

        print(f"💰 Nowy balans: {self.player_balance}")

    def to_response(self):
        """Konwertuj stan gry na format odpowiedzi API"""
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
