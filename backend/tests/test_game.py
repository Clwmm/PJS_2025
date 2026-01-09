import unittest
from unittest.mock import MagicMock, patch
from backend.game.deck.deck import Card
from backend.game.Game import GameState
from backend.services import RulesService, GameService, PlayerService


class TestRulesService(unittest.TestCase):
    """
    Testy logiki gry (RulesService).
    """

    def setUp(self):
        self.rules = RulesService.get_instance()

    def test_calculate_hand_normal(self):
        cards = [Card("5", "Hearts"), Card("9", "Clubs")]
        self.assertEqual(self.rules.calculate_hand(cards), 14)

    def test_calculate_hand_with_face_cards(self):
        cards = [Card("K", "Hearts"), Card("Q", "Clubs")]
        self.assertEqual(self.rules.calculate_hand(cards), 20)

    def test_calculate_hand_with_aces_adjusted(self):
        cards = [Card("A", "Hearts"), Card("9", "Clubs"), Card("5", "Spades")]
        self.assertEqual(self.rules.calculate_hand(cards), 15)

    def test_calculate_hand_multiple_aces(self):
        cards = [Card("A", "Hearts"), Card("A", "Clubs"), Card("9", "Spades")]
        self.assertEqual(self.rules.calculate_hand(cards), 21)


class TestGameService(unittest.TestCase):
    """
    Testy przebiegu gry (GameService).
    """

    def setUp(self):
        self.service = GameService.get_instance()
        self.player_service = PlayerService.get_instance()

        self.service.games.clear()
        self.player_service._balances.clear()

        self.username = "Tester"
        self.player_service.reset_balance(self.username)

    # PATCHUJEMY Deck W MIEJSCU UŻYCIA (backend.game.Game), A NIE DEFINICJI
    @patch('backend.game.Game.Deck')
    def test_start_game_deals_two_cards_each(self, MockDeck):
        mock_deck_instance = MockDeck.return_value
        mock_deck_instance.deal.side_effect = [
            [Card("10", "Hearts"), Card("9", "Spades")],
            [Card("5", "Clubs"), Card("6", "Diamonds")]
        ]

        game = self.service.create_game(self.username, 100)

        self.assertEqual(len(game.player_cards), 2)
        self.assertEqual(len(game.dealer_cards), 2)
        self.assertEqual(game.game_state, "pTurn")

    @patch('backend.game.Game.Deck')
    def test_start_game_blackjack_triggers_stand(self, MockDeck):
        mock_deck_instance = MockDeck.return_value
        # Blackjack dla gracza (A + K = 21)
        mock_deck_instance.deal.side_effect = [
            [Card("A", "Hearts"), Card("K", "Spades")],
            [Card("5", "Clubs"), Card("6", "Diamonds")]
        ]
        mock_deck_instance.deal_one.side_effect = [Card("2", "Clubs"), Card("10", "Hearts")]

        game = self.service.create_game(self.username, 100)

        self.assertEqual(game.game_state, "end")
        self.assertEqual(game.result, "player")

    @patch('backend.game.Game.Deck')
    def test_hit_adds_card(self, MockDeck):
        mock_deck_instance = MockDeck.return_value
        mock_deck_instance.deal.side_effect = [
            [Card("10", "Hearts"), Card("2", "Spades")],
            [Card("5", "Clubs"), Card("6", "Diamonds")]
        ]
        mock_deck_instance.deal_one.return_value = Card("5", "Clubs")

        self.service.create_game(self.username, 100)
        game = self.service.hit(self.username)

        self.assertEqual(len(game.player_cards), 3)
        self.assertEqual(game.game_state, "pTurn")

    @patch('backend.game.Game.Deck')
    def test_hit_busts_player(self, MockDeck):
        mock_deck_instance = MockDeck.return_value
        mock_deck_instance.deal.side_effect = [
            [Card("10", "Hearts"), Card("9", "Clubs")],  # 19
            [Card("5", "Spades"), Card("6", "Diamonds")]
        ]
        # Dobranie 5 daje bust (24)
        mock_deck_instance.deal_one.return_value = Card("5", "Spades")

        self.service.create_game(self.username, 100)
        game = self.service.hit(self.username)

        self.assertEqual(game.game_state, "end")
        self.assertEqual(game.result, "dealer")
        self.assertEqual(self.player_service.get_balance(self.username), 900)

    def test_hit_wrong_state(self):
        self.service.create_game(self.username, 100)
        game = self.service.get_game(self.username)
        game.game_state = "dTurn"

        with self.assertRaises(ValueError):
            self.service.hit(self.username)

    def test_stand_wrong_state(self):
        with self.assertRaises(ValueError):
            self.service.stand(self.username)

    @patch('backend.game.Game.Deck')
    def test_stand_dealer_hits_until_17(self, MockDeck):
        mock_deck_instance = MockDeck.return_value
        mock_deck_instance.deal.side_effect = [
            [Card("10", "Hearts"), Card("7", "Clubs")],  # player 17
            [Card("5", "Spades"), Card("6", "Diamonds")]  # dealer 11
        ]
        # Dealer draws 5 (16) -> hits again -> draws 2 (18) -> stop
        mock_deck_instance.deal_one.side_effect = [
            Card("5", "Hearts"),
            Card("2", "Clubs")
        ]

        self.service.create_game(self.username, 100)
        game = self.service.stand(self.username)

        self.assertEqual(game.game_state, "end")
        self.assertEqual(len(game.dealer_cards), 4)

    @patch('backend.game.Game.Deck')
    def test_stand_player_wins(self, MockDeck):
        mock_deck_instance = MockDeck.return_value
        mock_deck_instance.deal.side_effect = [
            [Card("10", "Hearts"), Card("9", "Clubs")],  # player 19
            [Card("5", "Spades"), Card("6", "Diamonds")]  # dealer 11
        ]
        mock_deck_instance.deal_one.side_effect = [
            Card("5", "Hearts"),
            Card("2", "Clubs")  # Dealer 18
        ]

        self.service.create_game(self.username, 100)
        game = self.service.stand(self.username)

        self.assertEqual(game.result, "player")
        self.assertEqual(self.player_service.get_balance(self.username), 1100)

    @patch('backend.game.Game.Deck')
    def test_stand_dealer_wins(self, MockDeck):
        mock_deck_instance = MockDeck.return_value
        mock_deck_instance.deal.side_effect = [
            [Card("10", "Hearts"), Card("6", "Clubs")],  # player 16
            [Card("10", "Spades"), Card("8", "Diamonds")]  # dealer 18
        ]

        self.service.create_game(self.username, 100)
        game = self.service.stand(self.username)

        self.assertEqual(game.result, "dealer")
        self.assertEqual(self.player_service.get_balance(self.username), 900)

    @patch('backend.game.Game.Deck')
    def test_stand_draw(self, MockDeck):
        mock_deck_instance = MockDeck.return_value
        mock_deck_instance.deal.side_effect = [
            [Card("10", "Hearts"), Card("7", "Clubs")],  # player 17
            [Card("10", "Spades"), Card("7", "Diamonds")]  # dealer 17
        ]

        self.service.create_game(self.username, 100)
        game = self.service.stand(self.username)

        self.assertEqual(game.result, "draw")
        self.assertEqual(self.player_service.get_balance(self.username), 1000)


class TestGameStateDTO(unittest.TestCase):
    def test_response_in_bet_state(self):
        state = GameState("Test", 0)
        r = state.to_response(1000)
        self.assertEqual(r["data"]["gameState"], "bet")
        self.assertEqual(r["data"]["playerBalance"], 1000)

    def test_response_in_pTurn_state(self):
        state = GameState("Test", 100)
        state.game_state = "pTurn"
        state.player_cards = [Card("10", "Hearts")]
        state.dealer_cards = [Card("A", "Spades"), Card("K", "Hearts")]

        r = state.to_response(1000)
        dealer_cards = r["data"]["dealer"]["cards"]
        self.assertTrue(dealer_cards[1]["hidden"])

    def test_response_in_end_state(self):
        state = GameState("Test", 100)
        state.game_state = "end"
        state.player_cards = [Card("10", "Hearts")]
        state.dealer_cards = [Card("A", "Spades")]
        state.result = "player"

        r = state.to_response(1000)
        self.assertEqual(r["data"]["result"], "player")
        self.assertFalse(r["data"]["dealer"]["cards"][0]["hidden"])


if __name__ == "__main__":
    unittest.main()