

class Card(object):

    def __init__(self, rank, value, suit, kingHearts):
        self.__rank = rank
        self.__value = value
        self.__suit = suit
        self.__kingHearts = kingHearts

    def __repr__(self):
        return f"<{self.__value} of {self.__suit} ({self.__rank})>"

    def __str__(self):
        return f"{self.__value} of {self.__suit}."

    def __lt__(self, other):
        return self.__rank < other.__rank

    def __eq__(self, other):
        return ((self.__suit == other.suit) and (self.value == other.value))

    def __ne__(self, other):
        return not(self.__eq__(other))

    def __gt__(self, other):
        return self.__rank > other.__rank

    @property
    def rank(self):
        return self.__rank

    @property
    def value(self):
        return self.__value

    @property
    def suit(self):
        return self.__suit

    def isKingHearts(self):
        return self.__kingHearts



