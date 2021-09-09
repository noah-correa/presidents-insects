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
        self.__passed = not cards
        self.__kingHearts = self.__isKingHearts()
        self.__tripSix = self.__isTripSix()

    def __str__(self):
        if self.__pid == 0:
            return "No Card."
        ret = f"Player ID = {self.pid} played cards: [ "
        if self.__passed:
            ret = f"Player ID = {self.pid} passed."
        else:
            for card in self.cards:
                ret += f"({str(card)}) "
            ret += f"], Rank: {self.rank}."
        return ret

    def __dict__(self):
        d = {}
        d['pid'] = self.__pid
        d['nCards'] = self.__nCards
        d['rank'] = self.__rank
        d['passed'] = self.__passed
        d['kingHearts'] = self.__isKingHearts()
        d['tripSix'] = self.__isTripSix()
        d['cards'] = []
        for card in self.__cards:
            d['cards'].append(card.__dict__)
        return d

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
    def passed(self):
        return self.__passed

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
