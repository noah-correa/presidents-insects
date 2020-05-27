from move import Move

class Player(object):

    __id = 0

    @classmethod
    def generate_id(cls):
        Player.__id += 1
        return Player.__id

    def __init__(self, name):
        self.__id = Player.generate_id()
        self.__name = name
        self.__role = "Citizen"
        self.__hand = []
        self.__move = []
        self.__moveRank = 0
        self.__passed = 0

    def __str__(self):
        return f"Player: {self.name}, ID: {self.id}, Role: {self.role}."

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

    def resetPassed(self):
        self.__passed = 0

    def setRole(self, role):
        self.__role = role

    def setHand(self, hand):
        self.__hand = hand
        self.sortHand()

    # Sorts the cards in the players hand by their rank
    def sortHand(self):
        self.__hand.sort(key=lambda x: x.rank)

    def printHand(self):
        ret = f"--- {self.name}'s hand ({self.role}) ---\n"
        for i in range(len(self.hand)):
            ret += f"{i+1}. {str(self.hand[i])}\n"
        print(ret)

    def addCardHand(self, card):
        self.hand.append(card)
        self.sortHand()

    # Adds a card from the players hand to their move cards
    def addCardMove(self, i):
        if self.move != [] and self.hand[i] != self.move[0]:
            self.hand.extend(self.move)
            self.move.append(self.hand[i])
            self.moveRank = self.hand[i].rank
            self.hand.pop(i)
            self.sortHand()
        else:
            self.move.append(self.hand[i])
            self.moveRank += self.hand[i].rank
            self.tripleSix()
            self.hand.pop(i)
            self.sortHand()

    # Commits the card(s) in players move to the pile
    def playTurn(self):
        ret = Move(self.id, self.move, self.moveRank)
        self.move = []
        self.moveRank = 0
        return ret

    # Player passes turn, if any cards were in move, they are added back to hand
    def passTurn(self):
        self.__passed = 1
        self.__hand.extend(self.move)
        self.sortHand()
        return []

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
    def addTwo(self, cards):
        for card in cards:
            self.addCardHand(card)

    # Updates player attributes if triple six is in move
    def tripleSix(self):
        if self.__isTripleSix(self.move) is True:
            self.moveRank = 62

    # Helper function to determine if cards in given list is triple sixes
    def __isTripleSix(self, cards):
        if len(cards) == 3:
            for card in cards:
                if card.value == 6:
                    continue
                else:
                    return False
            return True

