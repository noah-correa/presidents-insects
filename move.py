"""
move.py for Presidents and Insects Python Card Game
Noah Correa
"""

class Move():
    def __init__(self, pid, cards=None, rank=0):
        self.__pid = pid
        self.__cards = cards
        self.__nCards = 0 if cards is None else len(cards)
        self.__rank = rank
        self.__noMove = not cards
        self.__kingHearts = self.__isKingHearts()
        self.__tripSix = self.__isTripSix()

    def __repr__(self):
        if self.noMove:
            return "No Card."
        ret = f"Player ID = {self.pid} played cards: [ "
        if self.cards is None:
            ret = f"Player ID = {self.pid} passed."
        else:
            for card in self.cards:
                ret += f"({str(card)}) "
            ret += f"], Rank: {self.rank}."
        return ret

    def __str__(self):
        if self.noMove:
            return "No Card."
        return str([str(card) for card in self.cards])

    @property
    def pid(self):
        return self.__pid

    @property
    def cards(self):
        return self.__cards

    @property
    def nCards(self):
        return self.__nCards

    @property
    def rank(self):
        return self.__rank

    @property
    def noMove(self):
        return self.__noMove

    @property
    def kingHearts(self):
        return self.__kingHearts

    @property
    def tripSix(self):
        return self.__tripSix

    def __isKingHearts(self):
        if self.cards is None:
            return 0
        for card in self.cards:
            if card.kingHearts:
                return 1
        return 0

    def __isTripSix(self):
        if self.nCards >= 3:
            for i in range(self.nCards - 1):
                if self.cards[i].value == "6" and self.cards[i].value == self.cards[i+1].value:
                    self.__rank = 62
                    return 1
        return 0
