from deck import Deck
from player import Player
from bot import Bot
from card import Card

from random import sample


ROLES = ["President", "Vice-President", "Citizen", "Insect", "Giga-Insect"]

class Game(object):
    def __init__(self, players, total):
        self.__deck = Deck()
        self.__nTotal = total
        self.__nPlayers = players
        self.__nBots = total - players
        self.__players = {}
        self.__roles = {ROLES[0] : None, ROLES[1] : None, ROLES[2] : [], ROLES[3] : None, ROLES[4] : None}
        self.__nHand = 52//total
        self.__nSpare = 52%total
        self.__winners = []
        self.__roundNumber = 0
        self.__turnNumber = 0
        self.__currPlayer = -1
        self.__topMove = []


    @property
    def deck(self):
        return self.__deck

    @property
    def nTotal(self):
        return self.__nTotal

    @property
    def nPlayers(self):
        return self.__nPlayers

    @property
    def nBots(self):
        return self.__nBots

    @property
    def players(self):
        return self.__players

    @property
    def nHand(self):
        return self.__nHand

    @property
    def nSpare(self):
        return self.__nSpare

    @property
    def roles(self):
        return self.__roles

    @property
    def winners(self):
        return self.__winners

    @property
    def roundNumber(self):
        return self.__roundNumber

    @property
    def turnNumber(self):
        return self.__turnNumber

    @property
    def currPlayer(self):
        return self.__currPlayer
    
    @property
    def topMove(self):
        return self.__topMove

    # Returns id of given player name, returns -1 if not found
    def getPlayerId(self, name):
        for i in self.players:
            if self.players[i].name == name:
                return i
        return -1

    def __checkName(self, name):
        for id in self.players:
            if self.players[id].name == name:
                return 1
        return 0

    # Adds a new player to the game
    def addPlayers(self):
        for i in range(self.nBots):
            new_bot = Bot()
            self.players[new_bot.id] = new_bot
        for i in range(self.nPlayers):
            name = input(f"Enter name for player {i+1}: ")
            badName = self.__checkName(name)
            while badName:
                name = input(f"Name already taken. Please enter another name for player {i+1}: ")
                badName = self.__checkName(name)
            new_player = Player(name)
            self.players[new_player.id] = new_player
        self.updateRoles()

    # Deals hand to all players
    def dealHands(self):
        for i in range(self.nTotal):
            self.players[i+1].setHand(self.deck.deal(self.nHand))
        spares = sample(self.deck.spareCards(), len(self.deck.spareCards()))
        if len(spares) != self.nSpare:
            raise Exception("Too many spare cards in deck")
        else:
            if len(self.roles[ROLES[2]]) >= self.nSpare:
                citizens = sample(self.roles[ROLES[2]], self.nSpare)
                for i in range(len(citizens)):
                    self.players[citizens[i]].addCardHand(spares[i])
            else:
                citizens = sample(self.roles[ROLES[2]], len(self.roles[ROLES[2]]))
                for i in range(len(citizens)):
                    self.players[citizens[i]].addCardHand(spares[i])
                remaining = spares[len(citizens):]
                for i in range(len(remaining)):
                    self.players[self.roles[ROLES[i+3]]].addCardHand(remaining[i])
                    if i == 2:
                        self.players[self.roles[ROLES[1]]].addCardHand(remaining[i])

    # Updates roles dict in game class
    def updateRoles(self):
        self.__roles = {ROLES[0] : None, ROLES[1] : None, ROLES[2] : [], ROLES[3] : None, ROLES[4] : None}
        for id in self.players:
            if self.players[id].role == ROLES[2]:
                self.roles[self.players[id].role].append(id)
            else:
                self.roles[self.players[id].role] = id

    # Returns player id with 3 of clubs
    def __findFirstTurn(self):
        for id in self.players:
            for card in self.players[id].hand:
                if card.value == "3" and card.suit == "Clubs":
                    return id
        return -1

    def __resetHands(self):
        for id in self.players:
            self.players[id].setHand([])

    # Resets players passed flags for new round
    def __resetPassed(self):
        for id in self.players:
            self.players[id].resetPassed()

    # Resets deck for new round
    def __resetDeck(self):
        self.__deck = Deck()

    # Sets up for a new round
    def newRound(self):
        self.__resetPassed()
        self.__resetHands()
        self.__resetDeck()
        self.dealHands()
        if self.roundNumber != 0:
            self.players[self.roles[ROLES[0]]].addTwo(self.players[self.roles[ROLES[4]]].highTwo())
            self.players[self.roles[ROLES[4]]].addTwo(self.players[self.roles[ROLES[0]]].lowTwo())
            self.players[self.roles[ROLES[1]]].addCardHand(self.players[self.roles[ROLES[3]]].highOne())
            self.players[self.roles[ROLES[3]]].addCardHand(self.players[self.roles[ROLES[1]]].lowOne())
        self.__currPlayer = self.__findFirstTurn()
        self.__roundNumber += 1
        self.__turnNumber == 0
        print(f"\t=== ROUND {self.roundNumber} ===")

    # Finds id of player of next turn
    def nextTurnPlayer(self):
        id = self.currPlayer + 1
        for i in range(self.nTotal):
            if id > self.nTotal:
                id = 1
            if self.players[id].passed == 0 and self.players[id].nCards != 0:
                return id
            else:
                id += 1
        if id == self.currPlayer + 1:
            return 0

    def nextTurn(self):
        pass

        


    # Function to close application
    def exit(self):
        print("Thanks for playing!")
        exit()



game = Game(1, 7)
game.addPlayers()
game.newRound()
for i in game.players:
    game.players[i].printHand()
game.players[1].setRole(ROLES[0])
game.players[2].setRole(ROLES[1])
game.players[3].setRole(ROLES[3])
game.players[4].setRole(ROLES[4])
game.updateRoles()
game.newRound()
for i in game.players:
    game.players[i].printHand()



