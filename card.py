"""
card.py for Presidents and Insects Python Card Game
Noah Correa
"""

import pygame

class Card():

    def __init__(self, rank, value, suit):
        self.__rank = rank
        self.__value = value
        self.__suit = suit
        self.__kingHearts = self.__isKingHearts()
        self.__img = pygame.transform.scale(pygame.image.load("images/" + self.value + self.suit[0] + ".png"), (115, 176))
        self.__back = pygame.image.load("images/red_back.png")

    def __repr__(self):
        return f"<{self.__value} of {self.__suit} ({self.__rank})>"

    def __str__(self):
        return f"{self.__value} of {self.__suit}"

    def __lt__(self, other):
        return self.__rank < other.rank

    def __eq__(self, other):
        return (self.__suit == other.suit) and (self.value == other.value)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return self.__rank > other.rank

    @property
    def rank(self):
        return self.__rank

    @property
    def value(self):
        return self.__value

    @property
    def suit(self):
        return self.__suit

    @property
    def kingHearts(self):
        return self.__kingHearts

    @property
    def img(self):
        return self.__img

    def __isKingHearts(self):
        if self.suit == "Hearts" and self.value == "King":
            self.__rank = 61
            return 1
        else:
            return 0
