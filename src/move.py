

class Move(object):

    def __init__(self, id=0, cards=[], rank=0):
        self.__id = id
        self.__cards = cards
        self.__nCards = len(cards)
        self.__rank = rank

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
