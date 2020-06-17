from collections import defaultdict
from enum import IntEnum

class Strength(IntEnum):
    STRAIGHT_FLUSH = 8
    FOUR_KIND = 7
    FULL_HOUSE = 6
    FLUSH = 5
    STRAIGHT = 4
    THREE_KIND = 3
    TWO_PAIR = 2
    PAIR = 1
    HIGH_CARD = 0

class Hand:
    # assumes cards are from one deck when computing best hand
    def __init__(self, cards):
        self.cards = list(cards)
        self.cards.sort()
        self.best_hand = []
        self.strength = Strength.HIGH_CARD
        self.compute_best()

    def cmp_cards(self, other):
        for i in range(4, -1, -1):
            if self.best_hand[i].rank != other.best_hand[i].rank:
                return self.best_hand[i].rank - other.best_hand[i].rank
        return 0

    def cmp_hand(self, other):
        if self.strength == other.strength:
            if self.strength == Strength.STRAIGHT_FLUSH or self.strength == Strength.STRAIGHT:
                return self.best_hand[4].rank - other.best_hand[4].rank
            elif self.strength == Strength.FULL_HOUSE or self.strength == Strength.THREE_KIND or self.strength == Strength.FOUR_KIND:
                if self.best_hand[2].rank != other.best_hand[2].rank:
                    return self.best_hand[2].rank - other.best_hand[2].rank
            elif self.strength == Strength.TWO_PAIR:
                if self.best_hand[3].rank != other.best_hand[3].rank:
                    return self.best_hand[3].rank - other.best_hand[3].rank
                elif self.best_hand[1].rank != other.best_hand[1].rank:
                    return self.best_hand[1].rank - other.best_hand[1].rank
            elif self.strength == Strength.PAIR:
                self_pair = 0
                other_pair = 0
                for i in range(4, 0, -1):
                    if self.best_hand[i].rank == self.best_hand[i - 1].rank:
                        self_pair = self.best_hand[i].rank
                    if other.best_hand[i].rank == other.best_hand[i - 1].rank:
                        other_pair = other.best_hand[i].rank
                    if self_pair > 0 and other_pair > 0:
                        break
                if self_pair != other_pair:
                    return self_pair - other_pair
            return self.cmp_cards(other)
        return self.strength - other.strength

    # todo: add check for ace-low straight
    def straight_flush(self):
        suits = defaultdict(list)
        for card in reversed(self.cards):
            if len(suits[card.suit]) > 0 and card.rank < suits[card.suit][-1].rank - 1:
                suits[card.suit].clear()
            suits[card.suit].append(card)
            if len(suits[card.suit]) == 5:
                self.best_hand = suits[card.suit]
                self.best_hand.reverse()
                self.strength = Strength.STRAIGHT_FLUSH
                return True
        return False

    def four_kind(self):
        result = []
        for card in reversed(self.cards):
            if len(result) > 0 and card.rank != result[-1].rank:
                result.clear()
            result.append(card)
            if len(result) == 4:
                if self.cards[-1] in result:
                    self.best_hand = [self.cards[-5]] + result
                else:
                    self.best_hand = result + [self.cards[-1]]
                self.strength = Strength.FOUR_KIND
                return True
        return False

    def full_house(self):
        ranks = defaultdict(list)
        triple = 0
        pair = 0
        for card in reversed(self.cards):
            ranks[card.rank].append(card)
            if len(ranks[card.rank]) == 3:
                if pair == card.rank:
                    pair = 0
                triple = card.rank
            elif len(ranks[card.rank]) == 2 and pair == 0:
                pair = card.rank
            if triple > 0 and pair > 0:
                if triple > pair:
                    self.best_hand = ranks[card.rank] + ranks[triple]
                else:
                    self.best_hand = ranks[card.rank] + ranks[pair]
                self.strength = Strength.FULL_HOUSE
                return True
        return False

    def flush(self):
        suits = defaultdict(list)
        for card in reversed(self.cards):
            suits[card.suit].append(card)
            if len(suits[card.suit]) == 5:
                self.best_hand = suits[card.suit]
                self.best_hand.reverse()
                self.strength = Strength.FLUSH
                return True
        return False

    # todo: add check for ace-low straight
    def straight(self):
        stack = []
        for card in reversed(self.cards):
            if len(stack) > 0 and card.rank + 1 < stack[-1].rank:
                stack.clear()
            if len(stack) == 0 or card.rank + 1 == stack[-1].rank:
                stack.append(card)
            if len(stack) == 5:
                self.best_hand = stack
                self.best_hand.reverse()
                self.strength = Strength.STRAIGHT
                return True
        return False

    def three_kind(self):
        result = []
        highest = []
        for card in reversed(self.cards):
            if len(result) == 0 or card.rank == result[-1].rank:
                result.append(card)
            else:
                highest.append(card)
                if len(result) < 3:
                    result.clear()
                    result.append(card)
            if len(result) == 3 and len(highest) >= 2:
                self.best_hand = result + highest[:2]
                self.best_hand.sort()
                self.strength = Strength.THREE_KIND
                return True
        return False

    def two_pair(self):
        ranks = defaultdict(list)
        pairs = []
        highest = []
        for card in reversed(self.cards):
            ranks[card.rank].append(card)
            if len(ranks[card.rank]) == 1:
                highest.append(card)
            if len(ranks[card.rank]) == 2:
                pairs.append(card.rank)
                highest.pop()
            if len(pairs) == 2 and len(highest) > 0:
                self.best_hand = ranks[pairs[1]] + ranks[pairs[0]] + [highest[0]]
                self.best_hand.sort()
                self.strength = Strength.TWO_PAIR
                return True
        return False

    def pair(self):
        pair = []
        highest = []
        for card in reversed(self.cards):
            if len(pair) == 0:
                pair.append(card)
                highest.append(card)
            elif len(pair) == 2:
                highest.append(card)
            elif pair[0].rank == card.rank:
                highest.pop()
                pair.append(card)
            else:
                pair.pop()
                pair.append(card)
                highest.append(card)
            if len(pair) == 2 and len(highest) >= 3:
                self.best_hand = pair + highest[:3]
                self.best_hand.sort()
                self.strength = Strength.PAIR
                return True
        return False

    def high_card(self):
        self.best_hand = self.cards[-5:]
        self.strength = Strength.HIGH_CARD
        return True

    def compute_best(self):
        functions = [self.straight_flush, self.four_kind, self.full_house, self.flush, self.straight, self.three_kind, self.two_pair, self.pair, self.high_card]
        for i in range(len(functions)):
            if functions[i]():
                break

    def __repr__(self):
        res = str(self.strength) + ": "
        for card in self.best_hand:
            res += str(card)
        return res

    # def best_hand_prev(self):
    #     suits = set()
    #     ranks = defaultdict(int)
    #     for card in self.cards:
    #         suits.add(card.suit)
    #         ranks[card.rank] += 1
    #     rank_count = set(ranks.values())
    #     if len(suits) == 1 and len(rank_count) == 1 and self.cards[4].rank - self.cards[0].rank == 4:
    #         return Strength.STRAIGHT_FLUSH
    #     if 4 in set(rank_count):
    #         return Strength.FOUR_KIND
    #     if 3 in rank_count and 2 in rank_count:
    #         return Strength.FULL_HOUSE
    #     if len(suits) == 1:
    #         return Strength.FLUSH
    #     if len(rank_count) == 1 and self.cards[4].rank - self.cards[0].rank == 4:
    #         return Strength.STRAIGHT
    #     if 3 in rank_count:
    #         return Strength.THREE_KIND
    #     if 2 in rank_count and len(ranks) == 3:
    #         return Strength.TWO_PAIR
    #     if 2 in rank_count:
    #         return Strength.PAIR
    #     self.strength = Strength.HIGH_CARD
