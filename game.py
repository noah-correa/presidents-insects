import deck
import card
import player
import bot


class Game(object):
    def __init__(self, players, total):
        self.__deck = deck.Deck()
        self.__nTotal = total
        self.__nPlayers = players
        self.__nBots = total - players
        self.__players = []

    # 52//total = number of cards in each hand
    # 52%total = number of spare cards to deal

