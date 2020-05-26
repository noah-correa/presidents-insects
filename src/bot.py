from player import Player
from move import move

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
        self.__move = -1
        super().__init__(f"Bot {self.__idBot}")

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
    def move(self):
        return self.__move

    def decideMove(self, move):
        self.__groupHand()
        if move.nCards == 4:
            if self.quads != {}:
                for i in self.quads:
                    if self.quads[i].rank * 4 > move.rank:
                        self.__move = Move(self.id, self.hand[i:i+4], self.quads[i].rank * 4)
                        return
        elif 

    def __groupHand(self):
        self.__pairs = {}
        self.__trips = {}
        self.__quads = {}
        self.__tripSix = -1
        self.__kingHearts = -1
        for i in len(self.nCards):
            if i + 3 < len(self.nCards):
                if self.hand[i].value == self.hand[i+1].value: 
                    if self.hand[i].value == self.hand[i+2].value:
                        if self.hand[i].value == self.hand[i+3].value:
                            if i is not in self.pairs and i is not in self.trips:
                                self.__quads[i] = [i, i+1, i+2, i+3]
            if i + 2 < len(self.nCards):
                if self.hand[i].value == self.hand[i+1].value: 
                    if self.hand[i].value == self.hand[i+2].value:
                        if i is not in self.pairs and i is not in self.quads:
                            if self.hand[i].value == "6":
                                self.__tripSix = i
                            else:
                                self.__trips[i] = [i, i+1, i+2]
            if i + 1 < len(self.nCards):
                if self.hand[i].value == self.hand[i+1].value: 
                    if i is not in self.quads and i is not in self.trips:
                        self.__pairs[i] = [i, i+1]
            if self.hand[i].kingHearts:
                self.__kingHearts = i
