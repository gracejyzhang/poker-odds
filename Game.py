from Deck import Deck
from Hand import Hand
import itertools
import random

class Game:
    def __init__(self):
        self.deck = Deck()
        self.losses = 0
        self.wins = 0
        self.ties = 0
        self.percent = 1.0

    def compute_opp(self, my_hand):
        opp_combos = itertools.combinations(self.deck.deck, 2)
        for combo in opp_combos:
            if random.random() > self.percent:
                continue
            self.count += 1
            self.deck.init_opp(combo)
            opp_hand = Hand(self.deck.opp.union(self.deck.community))
            if my_hand.cmp_hand(opp_hand) > 0:
                self.wins += 1
            elif my_hand.cmp_hand(opp_hand) < 0:
                self.losses += 1
            else:
                self.ties += 1
            self.deck.reset_opp()

    def compute_comm(self):
        community_combos = itertools.combinations(self.deck.deck, 5 - len(self.deck.community))
        self.count = 0
        for combo in community_combos:
            if random.random() > self.percent:
                continue
            self.deck.add_comm(combo)
            my_hand = Hand(self.deck.hole.union(self.deck.community))
            self.compute_opp(my_hand)
            self.deck.remove_comm(combo)
        print(self.losses)
        print(self.count)

    # todo: add error and invalid input checks
    # returns (win_percent, tie_percent, loss_percent)
    def compute(self, hole, community, num_opp):
        self.deck.init_hole(hole)
        self.deck.add_comm(community)
        # add opp stuff
        self.compute_percent(2 * num_opp + 5 - len(community))
        self.compute_comm()
        return (self.wins / (self.wins + self.losses + self.ties),
                self.ties / (self.wins + self.losses + self.ties),
                self.losses / (self.wins + self.losses + self.ties))

    def compute_percent(self, num_unknown):
        if num_unknown > 3:
            self.percent = 0.16 * (0.2 ** (num_unknown - 4))
        # 0.15 for 4 cards
        # 0.04 for 5 cards
        # 0.01 for 6 cards

    # def compute_prev(self, hole, community, num_opp, percent = 1.0):
    #     self.deck.init_hole(hole)
    #     self.deck.add_comm(community)
    #     combos = itertools.combinations(self.deck.deck, 5 + 2 * num_opp - len(self.deck.community))
    #     num_iter = 0
    #     for combo in combos:
    #         if random.random() > percent:
    #             continue
    #         num_iter += 1
    #         community = set(itertools.combinations(combo, 5 - len(self.deck.community)))
    #         opp_hand = Hand(set(combo).union(self.deck.community))
    #         for entry in community:
    #             if random.random() > percent:
    #                 continue
    #             my_hand = Hand(self.deck.community.union(entry).union(self.deck.hole))
    #             cmp = my_hand.cmp_hand(opp_hand)
    #             if cmp >= 0:
    #                 self.win_count += 1
    #             if cmp <= 0:
    #                 self.lose_count += 1
    #     print(num_iter)
    #     return self.win_count / (self.win_count + self.lose_count)

