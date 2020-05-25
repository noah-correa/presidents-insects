

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
        return len(self.__hand) + len(self.__move)

    def setRole(self, role):
        self.__role = role

    def setHand(self, hand):
        self.__hand = hand
        self.sortHand()

    # Sorts the cards in the players hand by their rank
    def sortHand(self):
        self.__hand.sort(key=lambda x: x.rank)

    def printHand(self):
        ret = f"--- {self.__name}'s hand ---\n"
        for i in range(len(self.__hand)):
            ret += f"{i+1}. {str(self.__hand[i])}\n"
        print(ret)

    def addCardHand(self, card):
        self.hand.append(card)
        self.sortHand()

    # Adds a card from the players hand to their move cards
    def addCardMove(self, i):
        if self.__move is not None and self.__hand[i] != self.__move[0]:
            self.__hand.extend(self.__move)
            self.__move.append(self.__hand[i])
            self.__moveRank = self.__hand[i].rank
            self.__hand.pop(i)
            self.sortHand()
        else:
            self.__move.append(self.__hand[i])
            self.__moveRank += self.__hand[i].rank
            self.__hand.pop(i)
            self.sortHand()

    # Commits the card(s) in players move to the pile
    def playTurn(self):
        ret = self.__move
        self.__move = []
        return ret

    # Player passes turn, if any cards were in move, they are added back to hand
    def passTurn(self):
        self.__hand.extend(self.__move)
        self.sortHand()
        return []

    # Returns objectively lowest 2 cards in player's hand
    def lowTwo(self):
        ret = self.__hand[:2]
        self.__hand.pop(0)
        self.__hand.pop(1)
        return ret

    # Returns objectively highest 2 cards in player's hand
    def highTwo(self):
        ret = self.__hand[-2:]
        self.__hand.pop(-1)
        self.__hand.pop(-2)
        return ret

    # Updates player attributes if triple six is in move
    def tripleSix(self):
        if self.__isTripleSix(self.__move) is True:
            self.__moveRank = 62

    # Helper function to determine if cards in given list is triple sixes
    def __isTripleSix(self, cards):
        if len(cards) == 3:
            for card in cards:
                if card.value == 6:
                    continue
                else:
                    return False
            return True

