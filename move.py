

class Move(object):

    def __init__(self, id=0, cards=[], rank=0):
        self.__id = id
        self.__cards = cards
        self.__nCards = len(cards)
        self.__rank = rank
        self.__noMove = False if self.id != 0 else True
        self.__kingHearts = self.__isKingHearts()
        self.__tripSix = self.__isTripSix()

    def __str__(self):
        ret = f"ID: {self.id}, Cards = [ "
        for card in self.cards:
            ret += f"({str(card)}) "
        ret += f"], Rank: {self.rank}."
        return ret

    @property
    def id(self):
        return self.__id

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

    def __isKingHearts(self):
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

