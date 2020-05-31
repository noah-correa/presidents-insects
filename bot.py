"""
bot.py for Presidents and Insects Python Card Game
Noah Correa
"""

from player import Player

class Bot(Player):

    __idBot = 0

    @classmethod
    def generate_idBot(cls):
        Bot.__idBot += 1
        return Bot.__idBot

    def __init__(self):
        self.__idBot = Bot.generate_idBot()
        self.__pairs = {}
        self.__trips = {}
        self.__quads = {}
        self.__kingHearts = -1
        self.__tripSix = -1
        super().__init__(f"Bot {self.__idBot}")
        self.__isBot = 1

    @property
    def idBot(self):
        return self.__idBot

    @property
    def pairs(self):
        return self.__pairs

    @property
    def trips(self):
        return self.__trips

    @property
    def quads(self):
        return self.__quads

    @property
    def kingHearts(self):
        return self.__kingHearts

    @property
    def tripSix(self):
        return self.__tripSix

    def botPlayTurn(self, move):
        self.decideMove(move)
        if self.move == []:
            return self.passTurn()
        else:
            return self.playTurn()

    def decideMove(self, move):
        self.__groupHand()
        if move.noMove:
            self.addCardMove(0)
            return
        if move.nCards == 4 and self.quads != {}:
            for i in self.quads:
                if self.quads[i].rank * 4 > move.rank:
                    for j in range(4):
                        self.addCardMove(i+j)
                    return
        if move.nCards == 3 and self.trips != {}:
            for i in self.trips:
                if self.trips[i].rank * 3 > move.rank:
                    for j in range(3):
                        self.addCardMove(i+j)
                    return
        if move.nCards == 2 and self.pairs != {}:
            for i in self.pairs:
                if self.pairs[i].rank * 2 > move.rank:
                    for j in range(2):
                        self.addCardMove(i+j)
                    return
        if move.nCards == 1:
            for i in range(len(self.hand)):
                if self.hand[i].rank > move.rank:
                    self.addCardMove(i)
                    return
        if self.kingHearts != -1:
            self.addCardMove(self.kingHearts)
            return
        if self.tripSix != -1:
            for i in range(3):
                self.addCardMove(self.tripSix + i)
            return

    def __groupHand(self):
        self.__pairs = {}
        self.__trips = {}
        self.__quads = {}
        self.__tripSix = -1
        self.__kingHearts = -1
        for i in range(self.nCards):
            if i + 3 < self.nCards:
                if self.hand[i].value == self.hand[i+1].value:
                    if self.hand[i].value == self.hand[i+2].value:
                        if self.hand[i].value == self.hand[i+3].value:
                            if (i not in self.pairs) and (i not in self.trips):
                                self.__quads[i] = [i, i+1, i+2, i+3]
            if i + 2 < self.nCards:
                if self.hand[i].value == self.hand[i+1].value:
                    if self.hand[i].value == self.hand[i+2].value:
                        if i not in self.pairs and i not in self.quads:
                            if self.hand[i].value == "6":
                                self.__tripSix = i
                            else:
                                self.__trips[i] = [i, i+1, i+2]
            if i + 1 < self.nCards:
                if self.hand[i].value == self.hand[i+1].value:
                    if i not in self.quads and i not in self.trips:
                        self.__pairs[i] = [i, i+1]
            if self.hand[i].kingHearts:
                self.__kingHearts = i
