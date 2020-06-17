from Hand import Hand
from Card import Card
from Game import Game
import datetime

def test_game(hole_ranks, hole_suits, comm_ranks, comm_suits):
    start = datetime.datetime.now()
    hole = set()
    community = set()
    for i in range(2):
        hole.add(Card(hole_ranks[i], hole_suits[i]))
    for i in range(len(comm_ranks)):
        community.add(Card(comm_ranks[i], comm_suits[i]))
    game = Game()
    result = game.compute(hole, community, 1)
    print(datetime.datetime.now() - start)
    print(result)

def test_hand(ranks, suits):
    cards = []
    for i in range(len(ranks)):
        cards.append(Card(ranks[i], suits[i]))
    print(Hand(cards))

if __name__ == '__main__':
    test_game([13,14],['h', 'h'],[12,11],['h','h'])
    # test_hand([9,8,10,3,5,13,14], ['h','s','d','c','s','d','s'])

