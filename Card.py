from functools import total_ordering

# todo: add handling for invalid input
# todo: change suit and rank to enum
@total_ordering
class Card:
    # rank: 2 to 14 (ace)
    # suit: c (clubs), d (diamond), h (heart), s (spade)
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit.lower()

    def __hash__(self):
        return hash((self.rank, self.suit))

    def __eq__(self, other):
        return (self.rank, self.suit) == (other.rank, other.suit)

    def __ne__(self, other):
        return not(self == other)

    def __lt__(self, other):
        return (self.rank, self.suit) < (other.rank, other.suit)

    def __repr__(self):
        return str(self.rank) + self.suit
