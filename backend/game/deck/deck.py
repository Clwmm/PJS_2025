import random

class Card:
    """
    Represents a single playing card.
    """
    SUITS = ("Hearts", "Diamonds", "Clubs", "Spades")
    RANKS = ("2", "3", "4", "5", "6", "7", "8", "9", "10",
             "J", "Q", "K", "A")

    def __init__(self, rank, suit):
        if rank not in Card.RANKS:
            raise ValueError(f"Invalid rank: {rank}")
        if suit not in Card.SUITS:
            raise ValueError(f"Invalid suit: {suit}")
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"Card(rank='{self.rank}', suit='{self.suit}')"

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return (self.rank, self.suit) == (other.rank, other.suit)

    def __hash__(self):
        return hash((self.rank, self.suit))


class Deck:
    """
    Represents a standard game of 52 playing cards.
    """
    def __init__(self):
        self._cards = [
            Card(rank, suit)
            for suit in Card.SUITS
            for rank in Card.RANKS
        ]
        self.shuffle()

    def __len__(self):
        return len(self._cards)

    def __repr__(self):
        return f"Deck({len(self._cards)} cards)"

    def __iter__(self):
        # allows: for card in game:
        return iter(self._cards)

    def shuffle(self):
        random.shuffle(self._cards)

    def deal_one(self):
        """
        Deal (remove and return) one card from the top of the game.
        Raises IndexError if the game is empty.
        """
        if not self._cards:
            raise IndexError("Cannot deal from an empty game")
        return self._cards.pop()

    def deal(self, n):
        """
        Deal n cards and return them as a list.
        Raises ValueError if there are not enough cards.
        """
        if n < 0:
            raise ValueError("Number of cards to deal must be non-negative")
        if n > len(self._cards):
            raise ValueError("Not enough cards left in the game")
        dealt = self._cards[-n:]
        self._cards = self._cards[:-n]
        return dealt

    def reset(self):
        self.__init__()


# Example usage:
if __name__ == "__main__":
    deck = Deck()
    print(deck)               # Deck(52 cards)
    deck.shuffle()
    card = deck.deal_one()
    print("Dealt:", card)     # e.g. "Dealt: K of Hearts"
    print("Cards left:", len(deck))
    hand = deck.deal(5)
    print("Hand:", ", ".join(str(c) for c in hand))
    print(deck)
    deck.reset()
    print(deck)