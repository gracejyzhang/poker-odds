from MultiDeck import MultiDeck
from Hand import Hand
import random
from copy import deepcopy
from operator import add
from multiprocessing import Pool
from functools import partial

def combinations(iterable, size, num_iter):
    result = set()
    for i in range(num_iter):
        result.add(tuple(random.sample(iterable, size)))
    return result

class Game:
    def __init__(self):
        self.deck = MultiDeck()
        self.losses = 0
        self.wins = 0
        self.ties = 0
        self.percent = 1.0
        self.num_opps = 5
        self.comm_iter = 500
        self.opp_iter = [100,10,4,3,2,2,1,1,1]
        # 4 comm cards, round(opp_iter * 1.6) is good
        # 3 com cards,

    # returns num wins, num ties, num losses
    @staticmethod
    def parallel_opp(num_opps, percent, deck, my_hand, num_iter):
        if num_opps == 0:
            tie = False
            for opp_pair in deck.opps:
                opp_hand = Hand(deck.community.union(opp_pair))
                cmp = my_hand.cmp_hand(opp_hand)
                if cmp < 0:
                    return [0,0,1]
                elif cmp == 0:
                    tie = True
            if tie:
                return [0,1,0]
            else:
                return [1,0,0]
        else:
            opp_combos = combinations(deck.deck, 2, num_iter)
            results = [0,0,0]
            for combo in opp_combos:
                deck.init_opp(combo)
                results = list(map(add, results, Game.parallel_opp(num_opps - 1, percent, deck, my_hand, num_iter)))
                deck.del_opp()
            return results

    @staticmethod
    def parallel_process(deck, num_opps, percent, num_iter, community):
        my_deck = deepcopy(deck)
        my_deck.add_comm(community)
        my_hand = Hand(my_deck.hole.union(my_deck.community))
        return Game.parallel_opp(num_opps, percent, my_deck, my_hand, num_iter)

    def parallel_comm(self):
        pool = Pool()
        try:
            community_combos = combinations(self.deck.deck, 5 - len(self.deck.community), self.comm_iter)
            func = partial(Game.parallel_process, self.deck, self.num_opps, self.percent, self.opp_iter[self.num_opps - 1])
            results = pool.map(func, community_combos)
            total_results = [0,0,0]
            for result in results:
                total_results = list(map(add, total_results, result))
            self.wins = total_results[0]
            self.ties = total_results[1]
            self.losses = total_results[2]
        finally:
            pool.close()
            pool.join()

    # todo: add error and invalid input checks
    # returns (win_percent, tie_percent, loss_percent)
    def compute(self, hole, community):
        self.deck.init_hole(hole)
        self.deck.add_comm(community)
        # add opp stuff
        # self.compute_percent(2 * self.num_opps + 5 - len(community))
        self.parallel_comm()
        print(self.wins + self.losses + self.ties)
        return (self.wins / (self.wins + self.losses + self.ties),
                self.ties / (self.wins + self.losses + self.ties),
                self.losses / (self.wins + self.losses + self.ties))

    # def compute_percent(self, num_unknown):
    #     if num_unknown > 3:
    #         self.percent = 0.08 * (0.1 ** (min(num_unknown, 7) - 4))

    # def compute_comm(self):
    #     community_combos = itertools.combinations(self.deck.deck, 5 - len(self.deck.community))
    #     for combo in community_combos:
    #         if random.random() > self.percent:
    #             continue
    #         self.deck.add_comm(combo)
    #         my_hand = Hand(self.deck.hole.union(self.deck.community))
    #         self.compute_opp(my_hand)
    #         self.deck.remove_comm(combo)

    # def compute_opp(self, my_hand):
    #     opp_combos = itertools.combinations(self.deck.deck, 2)
    #     for combo in opp_combos:
    #         if random.random() > self.percent:
    #             continue
    #         self.deck.init_opp(combo)
    #         opp_hand = Hand(self.deck.opp.union(self.deck.community))
    #         cmp = my_hand.cmp_hand(opp_hand)
    #         if cmp > 0:
    #             self.wins += 1
    #         elif cmp < 0:
    #             self.losses += 1
    #         else:
    #             self.ties += 1
    #         self.deck.reset_opp()

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

