"""
game.py for Presidents and Insects Python Card Game
Noah Correa
"""

from random import sample

from deck import Deck
from player import Player
from bot import Bot
from move import Move

from card import Card

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
        self.__gameNumber = 0
        self.__roundNumber = 0
        self.__turnNumber = 0
        self.__currPlayer = 0
        self.__turnWinner = 0
        self.__topMove = Move(0)
        self.game_loop()


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

    @property
    def turnWinner(self):
        return self.__turnWinner

    @property
    def gameNumber(self):
        return self.__gameNumber

    # Returns id of given player name, returns -1 if not found
    def getPlayerId(self, name):
        for i in self.players:
            if self.players[i].name == name:
                return i
        return -1

    def __checkName(self, name):
        for ci in self.players:
            if self.players[ci].name == name:
                return 1
        return 0

    # Adds a new player to the game
    def addPlayers(self):
        # for i in range(self.nBots):
        #     new_bot = Bot()
        #     self.players[new_bot.id] = new_bot
        # for i in range(self.nPlayers):
        #     name = input(f"Enter name for player {i+1}: ")
        #     badName = self.__checkName(name)
        #     while badName:
        #         name = input(f"Name already taken. Please enter another name for player {i+1}: ")
        #         badName = self.__checkName(name)
        #     new_player = Player(name)
        #     self.players[new_player.id] = new_player
        # self.updateRoles()
        for i in range(self.nBots):
            new_bot = Bot()
            self.players[new_bot.id] = new_bot
        for i in range(self.nPlayers):
            new_player = Player(f"Player {i+1}")
            self.players[new_player.id] = new_player
        self.updateRoles()

    # Deals hand to all players
    def __dealHands(self):
        for i in range(self.nTotal):
            self.players[i+1].setHand(self.deck.deal(self.nHand))
        spares = sample(self.deck.spareCards(), len(self.deck.spareCards()))
        if len(spares) != self.nSpare:
            raise Exception("Too many spare cards in deck")
        else:
            if len(self.roles[ROLES[2]]) >= self.nSpare:
                citizens = sample(self.roles[ROLES[2]], self.nSpare)
                for i, pid in enumerate(citizens):
                    self.players[pid].addCardHand(spares[i])
            else:
                citizens = sample(self.roles[ROLES[2]], len(self.roles[ROLES[2]]))
                for i, pid in enumerate(citizens):
                    self.players[pid].addCardHand(spares[i])
                remaining = spares[len(citizens):]
                for i in range(len(remaining)):
                    self.players[self.roles[ROLES[i+3]]].addCardHand(remaining[i])
                    if i == 2:
                        self.players[self.roles[ROLES[1]]].addCardHand(remaining[i])

    # Updates roles dict in game class
    def updateRoles(self):
        self.__roles = {ROLES[0] : None, ROLES[1] : None, ROLES[2] : [], ROLES[3] : None, ROLES[4] : None}
        for i in self.players:
            if self.players[i].role == ROLES[2]:
                self.roles[self.players[i].role].append(i)
            else:
                self.roles[self.players[i].role] = i

    # Returns player id with 3 of clubs
    def __findFirstTurn(self):
        for i in self.players:
            for card in self.players[i].hand:
                if card.value == "3" and card.suit == "Clubs":
                    return i
        return -1

    def __resetHands(self):
        for i in self.players:
            self.players[i].setHand([])

    # Resets players passed flags for new round
    def __resetPassed(self):
        for i in self.players:
            self.players[i].resetPassed()

    # Resets deck for new round
    def __resetDeck(self):
        self.__deck = Deck()

    # Sets up for a new game (new deal of hands)
    def newGame(self):
        self.__resetPassed()
        self.__resetHands()
        self.__resetDeck()
        self.__dealHands()
        if self.roundNumber != 0:
            self.players[self.roles[ROLES[0]]].addTwo(self.players[self.roles[ROLES[4]]].highTwo())
            self.players[self.roles[ROLES[4]]].addTwo(self.players[self.roles[ROLES[0]]].lowTwo())
            self.players[self.roles[ROLES[1]]].addCardHand(self.players[self.roles[ROLES[3]]].highOne())
            self.players[self.roles[ROLES[3]]].addCardHand(self.players[self.roles[ROLES[1]]].lowOne())
        self.__currPlayer = self.__findFirstTurn()
        self.__roundNumber += 1
        self.__turnNumber = 0
        #print(f"\t=== ROUND {self.roundNumber} ===")

    # Sets up for a new round
    def newRound(self):
        self.__resetPassed()
        self.__resetHands()
        self.__resetDeck()
        self.__dealHands()
        if self.roundNumber != 0:
            self.players[self.roles[ROLES[0]]].addTwo(self.players[self.roles[ROLES[4]]].highTwo())
            self.players[self.roles[ROLES[4]]].addTwo(self.players[self.roles[ROLES[0]]].lowTwo())
            self.players[self.roles[ROLES[1]]].addCardHand(self.players[self.roles[ROLES[3]]].highOne())
            self.players[self.roles[ROLES[3]]].addCardHand(self.players[self.roles[ROLES[1]]].lowOne())
        self.__currPlayer = self.__findFirstTurn()
        self.__roundNumber += 1
        self.__turnNumber = 0
        #print(f"\t=== ROUND {self.roundNumber} ===")

    def resetTurn(self):
        # TODO
        pass


    # Finds id of player of next turn
    def nextTurnPlayer(self):
        pid = self.currPlayer + 1
        for i in range(self.nTotal):
            if pid > self.nTotal:
                pid = 1
            if self.players[pid].passed == 0 and self.players[pid].nCards != 0:
                return pid
            else:
                pid += 1
        if pid == self.currPlayer + 1:
            return 0

    def nextTurn(self):
        # TODO
        pass

    def validMove(self, move):
        if self.topMove.noMove and not move.noMove:
            return 1
        if move.nCards != self.topMove.nCards and (move.kingHeats or move.tripSix):
            return 1

        # TODO CHECK
        return 0

    def getUserInput(self, pid):
        while True:
            user_input = input("Which card do you want to add to your move? ")
            if user_input == "pass":
                return self.players[pid].passTurn()
            elif user_input == "play":
                return self.players[pid].playTurn()
            elif user_input == "q":
                self.exit()
            elif user_input == "":
                self.players[pid].printHand()
                self.players[pid].printMove()
            else:
                user_input = int(user_input) - 1
                self.players[pid].addCardMove(user_input)
                self.players[pid].printHand()
                self.players[pid].printMove()

    def addTopMove(self, move):
        if move.noMove:
            return
        self.__topMove = move
        return

    def game_loop(self):
        self.addPlayers()
        self.newGame()

        run = True
        while run:
            if isinstance(self.players[self.currPlayer], Bot):
                self.addTopMove(self.players[self.currPlayer].botPlayTurn(self.topMove))
            else:
                self.addTopMove(self.getUserInput(self.currPlayer))



    # Function to close application
    def exit(self):
        print("Thanks for playing!")
        exit()





print("\t=== President and Insects ===\n\t    --- By Noah Correa ---\n")

while True:
    total = input("Enter number of total players (5-7): ")
    try:
        total = int(total)
        if total < 5 or total > 7:
            print("Error: please enter a number between 5 and 7")
            continue
        break
    except ValueError:
        print("Error: please enter a valid number")
game = Game(1, total)


# for i in game.players:
#     game.players[i].printHand()

# game.players[7].addCardHand(Card(6, "6", "Clubs"))
# game.players[7].addCardHand(Card(6, "6", "Spades"))
# game.players[7].addCardHand(Card(6, "6", "Diamonds"))
# game.players[7].addCardHand(Card(6, "6", "Hearts"))
# game.players[7].printHand()
# while True:
#     pInput = input("Which card do you want to add to your move? ")
#     if pInput == "pass":
#         game.players[7].passTurn()
#     elif pInput == "play":
#         game.players[7].playTurn()
#     elif pInput == "q":
#         quit()
#     elif pInput == "":
#         game.players[7].printHand()
#         game.players[7].printMove()
#     else:
#         pInput = int(pInput) - 1
#         game.players[7].addCardMove(pInput)
#         game.players[7].printHand()
#         game.players[7].printMove()
