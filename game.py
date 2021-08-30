"""
game.py for Presidents and Insects Python Card Game
Noah Correa
"""

from random import sample

from deck import Deck
from player import Player
from bot import Bot
from move import Move


ROLES = ["President", "Vice-President", "Citizen", "Insect", "Giga-Insect"]

class Game(object):
    def __init__(self, players, total):
        self.__deck: Deck = Deck()
        self.__nTotal: int = total
        self.__nPlayers: int = players
        self.__nBots: int = total - players
        self.__players: dict = {}
        self.__roles: dict = {ROLES[0] : None, ROLES[1] : None, ROLES[2] : [], ROLES[3] : None, ROLES[4] : None}
        self.__nHand: int = 52//total
        self.__nSpare: int = 52%total
        self.__winners: list = []
        self.__gameNumber: int = 0
        self.__roundNumber: int = 0
        self.__turnNumber: int = 0
        self.__currPlayer: int = 0
        self.__topMove: Move = Move(0)

        self.addPlayers()
        # self.game_loop()

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
        # self.__updateRoles()
        for i in range(self.nBots):
            new_bot = Bot()
            self.players[new_bot.id] = new_bot
        for i in range(self.nPlayers):
            new_player = Player(f"Player {i+1}")
            self.players[new_player.id] = new_player
        self.__updateRoles()

    # Deals hand to all players
    def __dealHands(self):
        for _, player in self.players.items():
            player.setHand(self.deck.deal(self.nHand))
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
                for i, card in range(len(remaining)):
                    self.players[self.roles[ROLES[i+3]]].addCardHand(card)
                    if i == 2:
                        self.players[self.roles[ROLES[1]]].addCardHand(card)

    # Updates roles dict in game class
    def __updateRoles(self):
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

    def __updatePlayerRole(self):
        self.winners.append(self.__findLastPlayer())
        for i in range(self.nTotal):
            if i == 2:
                for j in range(self.nTotal - 4):
                    self.players[self.winners[i+j]].setRole(i)
            else:
                self.players[self.winners[i]].setRole(i)

    def __findLastPlayer(self):
        for i in self.players:
            if self.players[i].nCards != 0:
                return i
        return 0

    def __playersNumCards(self):
        ret = ""
        for i in self.players:
            ret += f"{self.players[i].name}: {self.players[i].nCards} cards. "
        return ret

    def __resetHands(self):
        for _, player in self.players.items():
            player.setHand([])

    # Resets players passed flags for new round
    def __resetPassed(self):
        for _, player in self.players.items():
            player.resetPassed()

    # Resets deck for new round
    def __resetDeck(self):
        self.__deck = Deck()

    # Sets up for a new game (new deal of hands)
    def newGame(self):
        self.__resetPassed()
        self.__resetHands()
        self.__resetDeck()
        self.__dealHands()
        if self.gameNumber != 0:
            self.players[self.roles[ROLES[0]]].addTwo(self.players[self.roles[ROLES[4]]].highTwo())
            self.players[self.roles[ROLES[4]]].addTwo(self.players[self.roles[ROLES[0]]].lowTwo())
            self.players[self.roles[ROLES[1]]].addCardHand(self.players[self.roles[ROLES[3]]].highOne())
            self.players[self.roles[ROLES[3]]].addCardHand(self.players[self.roles[ROLES[1]]].lowOne())

        self.__currPlayer = self.__findFirstTurn()
        self.__gameNumber += 1
        self.__roundNumber = 0
        self.__winners = []
        self.newRound()

    # Sets up for a new round
    def newRound(self):
        self.__resetPassed()
        self.__roundNumber += 1
        self.__turnNumber = 1
        self.__topMove = Move(0)


    # Finds id of player of next turn
    def nextTurnPlayer(self):
        pid = self.currPlayer
        for _ in range(1, self.nTotal):
            pid += 1
            if pid > self.nTotal:
                pid -= self.nTotal
            # print(f"--> Testing pid = {pid} ({self.players[pid].name})")
            if not self.players[pid].passed and pid not in self.winners and pid != self.topMove.pid and self.players[pid].nCards != 0:
                return pid

        if self.players[pid].nCards == 0:
            return self.nextDefaultPlayer()
        else:
            return 0

    def nextDefaultPlayer(self):
        pid = self.currPlayer
        for _ in range(1, self.nTotal):
            pid += 1
            if pid > self.nTotal:
                pid -= self.nTotal
            if self.players[pid].nCards != 0:
                return pid
        return 0



    # Checks if move is valid
    def validMove(self, move):
        if self.topMove.noMove:
            if move.noMove:
                return 0
            if self.roundNumber == 1:
                for card in move.cards:
                    if card.value == "3" and card.suit == "Clubs":
                        return 1
                return 0
            return 1
        if move.noMove:
            return 1
        if move.rank > self.topMove.rank:
            if move.nCards == self.topMove.nCards:
                return 1
            if move.kingHearts or move.tripSix:
                return 1
            return 0
        return 0

    def getUserInput(self):
        self.players[self.currPlayer].printHand()
        self.players[self.currPlayer].printMove()
        while True:
            user_input = input("Which card do you want to add to your move? ")
            if user_input == "pass":
                return self.players[self.currPlayer].passTurn()
            elif user_input == "play":
                return self.players[self.currPlayer].playTurn()
            elif user_input == "q":
                self.exit()
            elif user_input == "":
                print(f"\n\n\t=== GAME {self.gameNumber} - ROUND {self.roundNumber} - TURN {self.turnNumber} ===")
                print(self.__playersNumCards())
                print("Top of Pile:\n\t" + str(self.topMove) + f" played by {self.topMove.pid}")
                self.players[self.currPlayer].printHand()
                self.players[self.currPlayer].printMove()
            else:
                try:
                    user_input = int(user_input) - 1
                except ValueError:
                    print("\nInvalid input, please try again...\n")
                    continue
                if user_input >= len(self.players[self.currPlayer].hand) or user_input < 0:
                    print("\nInvalid card, please try again...\n")
                else:
                    self.players[self.currPlayer].addCardMove(user_input)
                    self.players[self.currPlayer].printHand()
                    self.players[self.currPlayer].printMove()

    def addTopMove(self, move):
        if move.noMove:
            return
        self.__topMove = move
        return


    def nextTurn(self):
        # TODO

        return

    def game_loop(self):
        # self.addPlayers()
        self.newGame()

        run = True
        while run:
            print(f"\n\n\t=== GAME {self.gameNumber} - ROUND {self.roundNumber} - TURN {self.turnNumber} ({self.players[self.currPlayer].name}) ===")
            print(self.__playersNumCards())
            print("Top of Pile:\n\t" + str(self.topMove) + f" played by {self.topMove.pid}")

            isValidMove = 0
            if isinstance(self.players[self.currPlayer], Bot):
                botMove = self.players[self.currPlayer].botPlayTurn(self.topMove)
                isValidMove = self.validMove(botMove)
                if isValidMove:
                    self.addTopMove(botMove)
                    print(f"Bot {self.players[self.currPlayer].id} has {self.players[self.currPlayer].nCards} cards left after playing:\n\t" + str(botMove))
                else:
                    print(f"Bot {self.players[self.currPlayer].id} played invalid move:\n\t" + str(botMove))

            else:
                while True:
                    playerMove = self.getUserInput()
                    isValidMove = self.validMove(playerMove)
                    if isValidMove:
                        break
                    print("\nMove invalid, please try again...\n")
                    self.players[self.currPlayer].addInvalidMove(playerMove)
                self.addTopMove(playerMove)
                print(f"Player has {self.players[self.currPlayer].nCards} cards left after playing:\n\t" + str(playerMove))

            if self.players[self.currPlayer].nCards == 0:
                print(f"==> {self.players[self.currPlayer].name} is now out in winners = {self.winners}")
                self.winners.append(self.currPlayer)
            if len(self.winners) == self.nTotal - 1:
                self.__updatePlayerRole()
                self.__updateRoles()
                self.newGame()
                continue

            next_pid = self.nextTurnPlayer()
            if next_pid == 0:
                self.__currPlayer = self.topMove.pid
                self.newRound()
            else:
                self.__currPlayer = next_pid
                self.__turnNumber += 1



    # Function to close application
    def exit(self):
        print("Thanks for playing!")
        exit()





# print("\t=== President and Insects ===\n\t    --- By Noah Correa ---\n")

# while True:
#     num = input("Enter number of total players (5-7): ")
#     try:
#         num = int(num)
#         if num < 5 or num > 7:
#             print("Error: please enter a number between 5 and 7")
#             continue
#         break
#     except ValueError:
#         print("Error: please enter a valid number")
# print("\n\nLOADING...\n\n")
# game = Game(1, num)


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
