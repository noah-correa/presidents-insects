from deck import Deck
from card import *
from player import *
from bot import Bot

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

    # Returns id of given player name, returns -1 if not found
    def getPlayerId(self, name):
        for i in self.players:
            if self.players[i].name == name:
                return i
        return -1

    # Adds a new player to the game
    def addPlayers(self):
        for i in range(self.nBots):
            new_bot = Bot()
            self.players[new_bot.id] = new_bot
        for i in range(self.nPlayers):
            name = input(f"Enter name for player {i+1}: ")
            for id in self.players:
                if name == self.players[id].name:
                    raise Exception("Name already taken.") 
            new_player = Player(name)
            self.players[new_player.id] = new_player
        self.updateRoles()

    # Deals hand to all players
    def dealHands(self):
        print(self.roles)
        print(self.players)
        for i in range(self.nTotal):
            self.players[i+1].setHand(self.deck.deal(self.nHand))
            print(f"DEALT ID: {i+1}")
        for i in range(self.nSpare):
            spares = sample(self.deck.spareCards(), len(self.deck.spareCards()))
            if len(spares) != self.nSpare:
                raise Exception("Too many spare cards in deck")
            else:
                if len(self.roles[ROLES[2]]) >= self.nSpare:
                    citizens = sample(self.roles[ROLES[2]], self.nSpare)
                    print(f"CITIZENS: {len(citizens)}")
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


                       

                        


    def updateRoles(self):
        self.__clearRoles()
        for id in self.players:
            if self.players[id].role == ROLES[2]:
                self.roles[self.players[id].role].append(id)
            else:
                self.roles[self.players[id].role] = id
    
    def __clearRoles(self):
        self.__roles = {ROLES[0] : None, ROLES[1] : None, ROLES[2] : [], ROLES[3] : None, ROLES[4] : None}

    def setPlayerRole(self, id, role):
        self.players[id].setRole(role)


game = Game(1, 7)
game.addPlayers()
game.dealHands()
#game.players[1].printHand()
for i in game.players:
    game.players[i].printHand()



