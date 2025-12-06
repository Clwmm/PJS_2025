import unittest
from backend.game.deck.deck import Card, Deck  # adjust import path depending on your project
import random


class TestCard(unittest.TestCase):

    def test_valid_card_creation(self):
        card = Card("A", "Hearts")
        self.assertEqual(card.rank, "A")
        self.assertEqual(card.suit, "Hearts")

    def test_invalid_rank(self):
        with self.assertRaises(ValueError):
            Card("15", "Hearts")

    def test_invalid_suit(self):
        with self.assertRaises(ValueError):
            Card("A", "InvalidSuit")

    def test_str_representation(self):
        card = Card("K", "Spades")
        self.assertEqual(str(card), "K of Spades")

    def test_repr_representation(self):
        card = Card("Q", "Diamonds")
        self.assertEqual(repr(card), "Card(rank='Q', suit='Diamonds')")

    def test_equality(self):
        c1 = Card("10", "Clubs")
        c2 = Card("10", "Clubs")
        c3 = Card("A", "Clubs")

        self.assertEqual(c1, c2)
        self.assertNotEqual(c1, c3)
        self.assertNotEqual(c1, "not a card")

    def test_hashing(self):
        c1 = Card("5", "Hearts")
        c2 = Card("5", "Hearts")
        card_set = {c1, c2}
        self.assertEqual(len(card_set), 1)


class TestDeck(unittest.TestCase):

    def test_initial_deck_size(self):
        deck = Deck()
        self.assertEqual(len(deck), 52)

    def test_shuffle_changes_order(self):
        deck1 = Deck()
        deck2 = Deck()

        # Ensure shuffle creates different orders randomly
        deck1.shuffle()
        deck2.shuffle()
        self.assertNotEqual(
            [str(c) for c in deck1],
            [str(c) for c in deck2],
            "Shuffling should randomize order"
        )

    def test_deal_one_reduces_size(self):
        deck = Deck()
        first_card = deck.deal_one()
        self.assertIsInstance(first_card, Card)
        self.assertEqual(len(deck), 51)

    def test_deal_one_empty(self):
        deck = Deck()
        for _ in range(52):
            deck.deal_one()
        with self.assertRaises(IndexError):
            deck.deal_one()

    def test_deal_n_cards(self):
        deck = Deck()
        cards = deck.deal(5)
        self.assertEqual(len(cards), 5)
        self.assertEqual(len(deck), 47)

    def test_deal_too_many_cards(self):
        deck = Deck()
        with self.assertRaises(ValueError):
            deck.deal(53)

    def test_deal_negative(self):
        deck = Deck()
        with self.assertRaises(ValueError):
            deck.deal(-1)

    def test_reset(self):
        deck = Deck()
        deck.deal(10)
        deck.reset()
        self.assertEqual(len(deck), 52)

    def test_iterable(self):
        deck = Deck()
        count = sum(1 for _ in deck)
        self.assertEqual(count, 52)


if __name__ == "__main__":
    unittest.main()
