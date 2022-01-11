'''
File:           player.py
Author:         Noah Correa
Date:           09/9/21
Description:    Presidents and Insects Player Class
'''

from src.move import Move
from src.card import Card

class Player():

    __id = 0

    @classmethod
    def generate_id(cls):
        Player.__id += 1
        return Player.__id
    
    @classmethod
    def reset_id(cls):
        Player.__id = 0

    def __init__(self, name: str, id=None, role="Citizen", hand=[], move=[], moveRank=0, passed=0):
        if id is None:
            self.__id: int = Player.generate_id()
        else:
            self.__id: int = id
        self.__name: str = name
        self.__role: str = role
        self.__hand: list[Card] = hand
        self.__move: list[Card] = move
        self.__moveRank: int = moveRank
        self.__passed: int = passed

    def __repr__(self):
        ret = f'id = {self.__id}\n'
        ret += f'name = {self.__name}\n'
        ret += f'role = {self.__role}\n'
        ret += f'hand = {self.__hand}\n'
        ret += f'move = {self.__move}\n'
        ret += f'moveRank = {self.__moveRank}\n'
        ret += f'passed = {self.__passed}\n'
        return ret

    def __str__(self):
        return f"Player: {self.name}, ID: {self.id}, Role: {self.role}."

    def __dict__(self):
        d = {}
        d['id'] = self.__id
        d['name'] = self.__name
        d['role'] = self.__role
        d['nCards'] = self.nCards
        d['hand'] = []
        for card in self.__hand:
            d['hand'].append(card.__dict__())
        d['move'] = []
        for card in self.__move:
            d['move'].append(card.__dict__())
        d['moveRank'] = self.__moveRank
        d['passed'] = self.__passed
        return d

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def role(self):
        return self.__role

    @property
    def hand(self):
        return self.__hand

    @property
    def move(self):
        return self.__move

    @property
    def nCards(self):
        return len(self.hand) + len(self.move)

    @property
    def moveRank(self):
        return self.__moveRank

    @property
    def passed(self):
        return self.__passed

    @property
    def isBot(self):
        return False

    def resetPassed(self):
        self.__passed = 0

    def setRole(self, role: str):
        self.__role = role

    def setHand(self, hand: list[Card]):
        self.__hand = hand
        self.sortHand()

    # Sorts the cards in the players hand by their rank
    def sortHand(self):
        self.__hand.sort(key=lambda x: x.rank)

    # Prints player's hand
    def printHand(self):
        ret = f"--- {self.name}'s hand ({self.role}) ---\n"
        for i in range(len(self.hand)):
            ret += f"{i+1}. {str(self.hand[i])}\n"
        print(ret)

    # Prints player's move
    def printMove(self):
        ret = f"--- {self.name}'s move ({self.role}) ---\n"
        for i in range(len(self.move)):
            ret += f"{i+1}. {str(self.move[i])}\n"
        print(ret)

    def addInvalidMove(self, move: list[Card]):
        if not move.passed:
            self.hand.extend(move.cards)
            self.sortHand()

    # Adds given card to player's hand
    def addCardHand(self, card: Card):
        self.hand.append(card)
        self.sortHand()

    # Adds a card from the players hand to their move cards
    def addCardMove(self, i: int):
        # print(f"{self.name} is trying to add index: {i} from hand={[str(card) for card in self.hand]} and move={[str(card) for card in self.move]}")
        if self.move != [] and self.hand[i].value != self.move[0].value:
            self.hand.extend(self.move)
            self.__move = [self.hand[i]]
            self.__moveRank = self.hand[i].rank
            self.hand.pop(i)
            self.sortHand()
        else:
            self.move.append(self.hand[i])
            self.__moveRank += self.hand[i].rank
            self.tripleSix()
            self.hand.pop(i)
            self.sortHand()

    def addCardMoveHand(self, card: Card):
        if self.move == []:
            return
        else:
            self.move.remove(card)
            self.hand.append(card)
            self.sortHand()
            self.tripleSix()
            if self.move == []:
                self.__moveRank = 0


    # Commits the card(s) in players move to the pile
    def playTurn(self):
        if self.move == []:
            self.passTurn()
        ret = Move(self.id, self.move, self.moveRank)
        self.__move = []
        self.__moveRank = 0
        #print(ret)
        return ret

    # Player passes turn, if any cards were in move, they are added back to hand
    def passTurn(self):
        self.__passed = 1
        self.__hand.extend(self.move)
        self.__move = []
        self.sortHand()
        return Move(self.id)

    # Returns objectively lowest card in player's hand
    def lowOne(self):
        ret = self.hand[0]
        self.hand.pop(0)
        return ret

    # Returns objectively lowest 2 cards in player's hand
    def lowTwo(self):
        ret = []
        ret.append(self.lowOne())
        ret.append(self.lowOne())
        return ret

    # Returns objectively highest card in player's hand
    def highOne(self):
        ret = self.hand[-1]
        self.hand.pop(-1)
        return ret

    # Returns objectively highest 2 cards in player's hand
    def highTwo(self):
        ret = []
        ret.append(self.highOne())
        ret.append(self.highOne())
        return ret

    # Adds two cards to players hand
    def addTwo(self, cards: list[Card]):
        for card in cards:
            self.addCardHand(card)

    # Updates player attributes if triple six is in move
    def tripleSix(self):
        if self.__isTripleSix(self.move) is True:
            self.__moveRank = 62

    # Helper function to determine if cards in given list is triple sixes
    def __isTripleSix(self, cards: list[Card]):
        if len(cards) == 3:
            for card in cards:
                if card.value == "6":
                    continue
                return False
            return True
