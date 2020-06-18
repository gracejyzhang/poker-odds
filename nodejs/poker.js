var Hand = require('pokersolver').Hand;

function combinations(array, size) {

    function p(t, i) {
        if (t.length === size) {
            result.push(t);
            return;
        }
        if (i + 1 > array.length) {
            return;
        }
        p(t.concat(array[i]), i + 1);
        p(t, i + 1);
    }

    var result = [];
    p([], 0);
    return result;
}

class Deck {
    constructor() {
        this.deck = ['2c','2d','2h','2s','3c','3d','3h','3s','4c','4d','4h','4s','5c','5d','5h','5s','6c','6d','6h','6s','7c','7d','7h','7s','8c','8d','8h','8s','9c','9d','9h','9s','Tc','Td','Th','Ts','Jc','Jd','Jh','Js','Qc','Qd','Qh','Qs','Kc','Kd','Kh','Ks','Ac','Ad','Ah','As'];
        this.hole = [];
        this.opp = [];
        this.community = [];
    }

    add_hole(cards) {
        for (const card of cards) {
            this.deck.splice(this.deck.indexOf(card), 1);
            this.hole.push(card)
        }
    }

    remove_hole(cards) {
        for (const card of cards) {
            this.hole.splice(this.hole.indexOf(card), 1)
            this.deck.push(card)
        }
    }

    add_community(cards) {
        for (const card of cards) {
            this.deck.splice(this.deck.indexOf(card), 1);
            this.community.push(card)
        }
    }

    remove_community(cards) {
        for (const card of cards) {
            this.community.splice(this.community.indexOf(card), 1)
            this.deck.push(card)
        }
    }

    add_opp(cards) {
        for (const card of cards) {
            this.deck.splice(this.deck.indexOf(card), 1);
            this.opp.push(card)
        }
    }

    remove_opp(cards) {
        for (const card of cards) {
            this.opp.splice(this.opp.indexOf(card), 1)
            this.deck.push(card)
        }
    }
}

class Game {
    constructor() {
        // do I use new??
        this.deck = new Deck();
        this.losses = 0;
        this.wins = 0;
        this.ties = 0;
        this.percent = 0.5;
    }

    compute_opp(my_hand) {
        const opp_combos = combinations(this.deck.deck, 2);
        for (const combo of opp_combos) {
            if (Math.random() > this.percent) {
                continue;
            }
            this.deck.add_opp(combo);
            const opp_hand = this.deck.community.concat(this.deck.opp);
            var winner = Hand.winners([my_hand, opp_hand]);
            if (winner.length > 1) {
                self.ties += 1;
            }
            else if (winner[0].equals(my_hand)) {
                self.wins += 1;
            }
            else {
                self.losses += 1;
            }
            this.deck.remove_opp(combo);
        }
    }

    compute_comm() {
        const comm_combos = combinations(this.deck.deck, 5 - this.deck.community.length);
        for (const combo of comm_combos) {
            if (Math.random() > this.percent) {
                continue;
            }
            this.deck.add_community(combo);
            this.compute_opp(this.deck.hole.concat(this.deck.community));
            this.deck.remove_community(combo);
        }
    }

    compute() {
        this.compute_comm();
        return this.wins / (this.wins + this.losses + this.ties);
    }
}

game = new Game();
game.deck.add_hole(['As','Ad']);
game.deck.add_community(['Ac','Ah','Kh']);
console.log(game.compute());
