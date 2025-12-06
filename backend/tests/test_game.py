import unittest
from unittest.mock import MagicMock
from backend.game.deck.deck import Card, Deck
from backend.game.Game import GameState


class TestGameState(unittest.TestCase):

    def setUp(self):
        self.state = GameState("Tester", bet=100, balance=1000)

    # -------------------------------
    # calculate_hand tests
    # -------------------------------
    def test_calculate_hand_normal(self):
        cards = [Card("5", "Hearts"), Card("9", "Clubs")]
        self.assertEqual(self.state.calculate_hand(cards), 14)

    def test_calculate_hand_with_face_cards(self):
        cards = [Card("K", "Hearts"), Card("Q", "Clubs")]
        self.assertEqual(self.state.calculate_hand(cards), 20)

    def test_calculate_hand_with_aces_adjusted(self):
        cards = [Card("A", "Hearts"), Card("9", "Clubs"), Card("5", "Spades")]
        # A(11) + 9 + 5 = 25 → A becomes 1 → total = 15
        self.assertEqual(self.state.calculate_hand(cards), 15)

    def test_calculate_hand_multiple_aces(self):
        cards = [Card("A", "Hearts"), Card("A", "Clubs"), Card("9", "Spades")]
        # 11 + 11 + 9 = 31 → two adjustments: 31-10=21 → OK
        self.assertEqual(self.state.calculate_hand(cards), 21)

    # -------------------------------
    # start_game() tests
    # -------------------------------
    def test_start_game_deals_two_cards_each(self):
        # Mock deck.deal so we get deterministic cards
        self.state.deck.deal = MagicMock(side_effect=[
            [Card("10", "Hearts"), Card("9", "Spades")],  # player
            [Card("5", "Clubs"), Card("6", "Diamonds")]  # dealer
        ])

        self.state.start_game()

        self.assertEqual(len(self.state.player_cards), 2)
        self.assertEqual(len(self.state.dealer_cards), 2)
        self.assertEqual(self.state.game_state, "pTurn")

    def test_start_game_blackjack_triggers_stand(self):
        self.state.deck.deal = MagicMock(side_effect=[
            [Card("A", "Hearts"), Card("K", "Spades")],  # blackjack
            [Card("5", "Clubs"), Card("6", "Diamonds")]
        ])

        # Mock stand so we don't run its logic fully
        self.state.stand = MagicMock()

        self.state.start_game()
        self.state.stand.assert_called_once()  # blackjack auto-stand

    # -------------------------------
    # hit() tests
    # -------------------------------
    def test_hit_adds_card(self):
        self.state.game_state = "pTurn"
        self.state.player_cards = [Card("10", "Hearts")]
        self.state.deck.deal_one = MagicMock(return_value=Card("5", "Clubs"))

        self.state.hit()

        self.assertEqual(len(self.state.player_cards), 2)

    def test_hit_busts_player(self):
        self.state.game_state = "pTurn"
        self.state.player_cards = [Card("10", "Hearts"), Card("9", "Clubs")]
        self.state.deck.deal_one = MagicMock(return_value=Card("5", "Spades"))

        self.state.hit()

        self.assertEqual(self.state.game_state, "end")
        self.assertEqual(self.state.result, "dealer")
        self.assertEqual(self.state.player_balance, 900)

    def test_hit_wrong_state(self):
        self.state.game_state = "dTurn"
        with self.assertRaises(ValueError):
            self.state.hit()

    # -------------------------------
    # stand() tests
    # -------------------------------
    def test_stand_wrong_state(self):
        self.state.game_state = "bet"
        with self.assertRaises(ValueError):
            self.state.stand()

    def test_stand_dealer_hits_until_17(self):
        self.state.game_state = "pTurn"
        self.state.player_cards = [Card("10", "Hearts"), Card("7", "Clubs")]
        self.state.dealer_cards = [Card("5", "Spades"), Card("6", "Diamonds")]

        # Dealer draws 5 → 5+6+5 = 16 → draws again 2 → total 18 stop
        self.state.deck.deal_one = MagicMock(side_effect=[
            Card("5", "Hearts"),
            Card("2", "Clubs")
        ])

        self.state.stand()

        self.assertEqual(self.state.game_state, "end")
        self.assertEqual(len(self.state.dealer_cards), 4)

    def test_stand_player_wins(self):
        self.state.game_state = "pTurn"
        self.state.player_cards = [Card("10", "Hearts"), Card("9", "Clubs")]
        self.state.dealer_cards = [Card("5", "Spades"), Card("6", "Diamonds")]

        # Dealer draws 5 → 5+6+5 = 16 → draws 2 → 18
        self.state.deck.deal_one = MagicMock(side_effect=[
            Card("5", "Hearts"),
            Card("2", "Clubs")
        ])

        self.state.stand()

        self.assertEqual(self.state.result, "player")
        self.assertEqual(self.state.player_balance, 1100)

    def test_stand_dealer_wins(self):
        self.state.game_state = "pTurn"
        self.state.player_cards = [Card("10", "Hearts"), Card("6", "Clubs")]  # total 16
        self.state.dealer_cards = [Card("10", "Spades"), Card("8", "Diamonds")]  # total 18

        self.state.stand()

        self.assertEqual(self.state.result, "dealer")
        self.assertEqual(self.state.player_balance, 900)

    def test_stand_draw(self):
        self.state.game_state = "pTurn"
        self.state.player_cards = [Card("10", "Hearts"), Card("7", "Clubs")]
        self.state.dealer_cards = [Card("10", "Spades"), Card("7", "Diamonds")]

        self.state.stand()

        self.assertEqual(self.state.result, "draw")
        self.assertEqual(self.state.player_balance, 1000)

    # -------------------------------
    # to_response() tests
    # -------------------------------
    def test_response_in_bet_state(self):
        r = self.state.to_response()
        self.assertEqual(r["data"]["gameState"], "bet")
        self.assertEqual(r["data"]["playerBalance"], 1000)

    def test_response_in_pTurn_state(self):
        self.state.game_state = "pTurn"
        self.state.player_cards = [Card("10", "Hearts")]
        self.state.dealer_cards = [Card("A", "Spades"), Card("K", "Hearts")]

        r = self.state.to_response()
        dealer_cards = r["data"]["dealer"]["cards"]

        self.assertTrue(dealer_cards[1]["hidden"])  # hidden card in player's turn

    def test_response_in_end_state(self):
        self.state.game_state = "end"
        self.state.player_cards = [Card("10", "Hearts")]
        self.state.dealer_cards = [Card("A", "Spades")]
        self.state.result = "player"

        r = self.state.to_response()

        self.assertEqual(r["data"]["result"], "player")
        self.assertEqual(r["data"]["playerBalance"], 1000)
        self.assertFalse(r["data"]["dealer"]["cards"][0]["hidden"])


if __name__ == "__main__":
    unittest.main()
