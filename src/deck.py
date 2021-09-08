"""
deck.py for Presidents and Insects Python Card Game
Noah Correa
"""

import random
import pygame

from src.card import Card, CARD_H, CARD_W

class Deck(object):
    def __init__(self):
        self.__deck = []
        self.__dealt = []
        self.__cardBack = pygame.transform.scale(pygame.image.load("resources/cards/red_back.png"), (CARD_W, CARD_H))

        suits = ["Clubs", "Spades", "Diamonds", "Hearts"]
        for suit in suits:
            for rank in range(2, 15):
                if rank == 2:
                    value = str(rank)
                    rank = 15
                elif rank == 11:
                    value = "Jack"
                elif rank == 12:
                    value = "Queen"
                elif rank == 13:
                    value = "King"
                elif rank == 14:
                    value = "Ace"
                else:
                    value = str(rank)
                self.__deck.append(Card(rank, value, suit))

    def __str__(self):
        return f"Deck has {len(self.__deck)} cards and has dealt {len(self.__dealt)} cards."

    @property
    def deck(self):
        return self.__deck

    @property
    def dealt(self):
        return self.__dealt

    def printDeck(self):
        ret = ""
        for i in self.__deck:
            ret += f"{i}\n"
        return ret

    def printDealt(self):
        ret = ""
        for i in self.__dealt:
            ret += f"{i}\n"
        return ret

    def getCard(self, index):
        return self.__deck[index]

    def getCardBack(self):
        return self.__cardBack

    # Deal a hand of n cards from deck
    def deal(self, n):
        remaining_cards = [card for card in self.__deck if card not in self.__dealt]
        hand_index = random.sample(range(len(remaining_cards)-1), n)
        hand = []
        for i in hand_index:
            hand.append(remaining_cards[i])
            self.__dealt.append(remaining_cards[i])
        return hand

    def spareCards(self):
        return [card for card in self.__deck if card not in self.__dealt]
