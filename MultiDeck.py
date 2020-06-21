from Card import Card

# todo: add error and invalid input checking
# todo: add support for multiple opponents
# todo: add support for opponent ranges
class MultiDeck:
    def __init__(self):
        self.deck = self.init_deck()
        self.community = set()
        self.hole = set()
        self.opps = []

    def init_deck(self):
        deck = set()
        for rank in range(2, 15):
            for suit in ['h', 's', 'c', 'd']:
                deck.add(Card(rank, suit))
        return deck

    def init_hole(self, cards):
        self.deck.difference_update(cards)
        self.hole.update(cards)

    def add_comm(self, cards):
        self.deck.difference_update(cards)
        self.community.update(cards)

    def remove_comm(self, cards):
        self.community.difference_update(cards)
        self.deck.update(cards)

    def init_opp(self, cards):
        self.deck.difference_update(cards)
        self.opps.append(cards)

    def del_opp(self):
        self.deck.update(self.opps[-1])
        self.opps.pop()
