"""
game.py for Presidents and Insects Python Card Game
Noah Correa
"""
import sys
from random import sample

from src.deck import Deck
from src.player import Player
from src.bot import Bot
from src.move import Move


ROLES = ['President', 'Vice-President', 'Citizen', 'Insect', 'Giga-Insect']

class Game(object):
    def __init__(self):
        self.__deck: Deck = Deck()
        self.__nTotal: int = 0 
        self.__nPlayers: int = 0
        self.__nBots: int = 0
        self.__players: dict[int, Player] = {}
        self.__roles: dict = {ROLES[0] : None, ROLES[1] : None, ROLES[2] : [], ROLES[3] : None, ROLES[4] : None}
        self.__nHand: int = 0
        self.__nSpare: int = 0
        self.__winners: list = []
        self.__gameNumber: int = 0
        self.__roundNumber: int = 0
        self.__turnNumber: int = 0
        self.__currPlayer: int = 0
        self.__topMove: Move = Move(0)

        Player.reset_id()
        Bot.reset_id()
        # self.addPlayers()
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
    def getPlayerId(self, name) -> int:
        for i in self.players:
            if self.players[i].name == name:
                return i
        return -1

    def __checkName(self, name) -> bool:
        for ci in self.players:
            if self.players[ci].name == name:
                return True
        return False

    def startSP(self, total):
        self.__nTotal = total
        self.__nPlayers = 1
        self.__nBots = total-1
        self.__nHand = 52//self.__nTotal
        self.__nSpare = 52%self.__nTotal

        for _ in range(self.nBots):
            new_bot = Bot()
            self.players[new_bot.id] = new_bot

        new_player = Player(f"Player 1")
        self.players[new_player.id] = new_player
        self.__updatePlayerRoles()
        self.newGame()
        return

    def startMP(self):
        self.__nBots = 0
        self.__nTotal = self.__nPlayers
        self.__nHand = 52//self.__nTotal
        self.__nSpare = 52%self.__nTotal
        self.__updatePlayerRoles()
        self.newGame()
        return


    def addNewPlayer(self, name) -> bool:
        notvalid = self.__checkName(name)
        if notvalid:
            return False
        else:
            newPlayer = Player(name)
            self.players[newPlayer.id] = newPlayer
            self.__nPlayers += 1
            return True


    # Deals hand to all players
    def __dealHands(self) -> None:
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
                for i, card in enumerate(remaining):
                    self.players[self.roles[ROLES[i+3]]].addCardHand(card)
                    if i == 2:
                        self.players[self.roles[ROLES[1]]].addCardHand(card)

    # Returns player id with 3 of clubs
    def __findFirstTurn(self) -> None:
        for i in self.players:
            for card in self.players[i].hand:
                if card.value == "3" and card.suit == "Clubs":
                    return i
        return -1
    
    # TODO: Combine and fix updateRoles and updatePlayerRoles
    # Updates roles dict in game class
    # def __updateRoles(self) -> None:
    #     self.__roles = {ROLES[0] : None, ROLES[1] : None, ROLES[2] : [], ROLES[3] : None, ROLES[4] : None}
    #     for player in self.players.values():
    #         if player.role == ROLES[2]:
    #             self.roles[player.role].append(player.id)
    #         else:
    #             self.roles[player.role] = player.id


    def __updatePlayerRoles(self) -> None:
        if self.gameNumber != 0:
            self.winners.append(self.__findLastPlayer())
            # print(f"winners order: {self.winners}")
            self.players[self.winners[0]].setRole(ROLES[0])
            self.players[self.winners[1]].setRole(ROLES[1])
            self.players[self.winners[-2]].setRole(ROLES[-2])
            self.players[self.winners[-1]].setRole(ROLES[-1])
            for pid in self.winners[2:-2]:
                self.players[pid].setRole(ROLES[2])
        
        self.__roles[ROLES[2]] = []
        for player in self.players.values():
            if player.role == ROLES[2]:
                self.roles[player.role].append(player.id)
            else:
                self.roles[player.role] = player.id


    def __findLastPlayer(self) -> int:
        for player in self.players.values():
            if player.nCards != 0:
                return player.id
        return 0

    ### TERMINAL VERSION FUNCTION
    def __playersNumCards(self):
        ret = ""
        for i in self.players:
            ret += f"{self.players[i].name}: {self.players[i].nCards} cards. "
        return ret

    def __resetHands(self) -> None:
        for _, player in self.players.items():
            player.setHand([])

    # Resets players passed flags for new round
    def __resetPassed(self) -> None:
        for _, player in self.players.items():
            player.resetPassed()

    # Resets deck for new round
    def __resetDeck(self) -> None:
        self.__deck = Deck()

    # Sets up for a new game (new deal of hands)
    def newGame(self) -> None:
        if self.gameNumber != 0:
            self.__updatePlayerRoles()
        self.__resetPassed()
        self.__resetHands()
        self.__resetDeck()
            # self.__updateRoles()
        self.__dealHands()    
        if self.gameNumber != 0:
            highTwo = self.players[self.roles[ROLES[4]]].highTwo()
            lowTwo = self.players[self.roles[ROLES[0]]].lowTwo()
            highOne = self.players[self.roles[ROLES[3]]].highOne()
            lowOne = self.players[self.roles[ROLES[1]]].lowOne()
            # print(f"[{self.roles[ROLES[4]]}] gave high 2: {highTwo} to [{self.roles[ROLES[0]]}]")
            # print(f"[{self.roles[ROLES[0]]}] gave low 2: {lowTwo} to [{self.roles[ROLES[4]]}]")
            # print(f"[{self.roles[ROLES[3]]}] gave high 1: {highOne} to [{self.roles[ROLES[1]]}]")
            # print(f"[{self.roles[ROLES[1]]}] gave low 1: {lowOne} to [{self.roles[ROLES[3]]}]")
            self.players[self.roles[ROLES[0]]].addTwo(highTwo)
            self.players[self.roles[ROLES[4]]].addTwo(lowTwo)
            self.players[self.roles[ROLES[1]]].addCardHand(highOne)
            self.players[self.roles[ROLES[3]]].addCardHand(lowOne)
        # else:
        self.__currPlayer = self.__findFirstTurn()
        self.__gameNumber += 1
        self.__roundNumber = 0
        self.__winners = []
        self.newRound()

    # Sets up for a new round
    def newRound(self) -> None:
        self.__resetPassed()
        self.__roundNumber += 1
        self.__turnNumber = 1
        self.__topMove = Move(0)


    # Finds id of player of next turn
    def nextTurnPlayer(self) -> int:
        pid = self.currPlayer
        # print(f"-->current player = {pid}")

        # Checks if someone who didnt play the last move hasnt passed and has cards
        for _ in range(1, self.nTotal):
            pid += 1
            if pid > self.nTotal:
                pid -= self.nTotal
            # print(f"--> Testing pid = {pid} ({self.players[pid].name})")
            if not self.players[pid].passed and self.players[pid].nCards != 0 and pid != self.topMove.pid:
                # print(f"--> Valid player found: {pid}")
                return pid
        # print(f"\t--> No valid player found, next round")
        return 0


    # Finds id of next player if current player is now out
    def nextDefaultPlayer(self) -> int:

        if self.players[self.topMove.pid].nCards != 0:
            return self.topMove.pid

        pid = self.topMove.pid
        # print(f"\t--> current player = {pid}")
        for _ in range(1, self.nTotal):
            pid += 1
            if pid > self.nTotal:
                pid -= self.nTotal
            
            # print(f"\t--> testing player = {pid} ({self.players[pid].nCards} cards left)")
            if self.players[pid].nCards != 0:
                # print(f"\t--> returning {pid}")
                return pid
        return 0


    # Gets the current player Object
    def getCurrentPlayer(self) -> Player:
        return self.players[self.__currPlayer]

    
    # Gets the player object by name
    def getPlayer(self, name) -> Player:
        pid = self.getPlayerId(name)
        if pid != -1:
            return self.players[pid]
        return None

    # Checks if move is valid
    def validMove(self, move: Move) -> bool:
        if self.topMove.pid == 0:
            if move.pid == 0:
                return False
            if self.roundNumber == 1:
                if move.cards is None:
                    return False
                for card in move.cards:
                    if card.value == "3" and card.suit == "Clubs":
                        return True
                return False
            if move.passed:
                return False
            return True
        if move.passed:
            return True
        if move.rank > self.topMove.rank:
            if move.nCards == self.topMove.nCards:
                return True
            if move.kingHearts or move.tripSix:
                return True
            return False
        return False

    # Checks if player's current move cards are valid
    def playerValidMove(self, player: Player) -> bool:
        if player.move == []:
            return False
        testMove = Move(player.id, player.move, player.moveRank)
        return self.validMove(testMove)
        
    # Adds the new move to top of pile
    def addTopMove(self, move) -> None:
        # print(f"\t{move}")
        if not move.passed:
            self.__topMove = move

    # Updates Game object for next turn
    def nextTurn(self) -> None:
        print(f"==== Game {self.gameNumber}, Round {self.roundNumber}, Turn {self.turnNumber} ====")
        print(self.topMove)
        # for player in self.players.values():
        #     print(f"{player.role} {player.name} has {player.nCards} cards remaining at the start of the round")

        # Check if player who played move is not out
        if self.players[self.currPlayer].nCards == 0:
            self.winners.append(self.currPlayer)
            # print(f"==> {self.players[self.currPlayer].name} is now out in winners = {self.winners}")

        # Check if only 1 player remains
        if len(self.winners) == self.nTotal - 1:
            # print("==> Only 1 player left, starting next game")
            # Set game to be over
            # self.__updatePlayerRoles()
            # self.__updateRoles()
            self.newGame()
            return


        # Otherwise, get the next player
        next_pid = self.nextTurnPlayer()
        # Check if no next player
        if next_pid == 0:
            # print("==> no next player")
            # If no next player, start next round
            self.__currPlayer = self.nextDefaultPlayer()
            self.newRound()
        else:
            # print(f"==>next player: {self.players[next_pid]}")
            # Otherwise, go to next player
            self.__currPlayer = next_pid
            self.__turnNumber += 1
        return

    # Function to close application
    def exit(self) -> None:
        print("Thanks for playing!")
        sys.exit()


    def getPlayersNumCards(self):
        ret = ''
        for player in self.players.values():
            ret += f'{player.role} {player.name}: {player.nCards}, '
        return ret[:-2]

    def __str__(self):
        # ret = f'GAME\n\t->gameNumber={self.gameNumber}\n\t->gameNumber={self.gameNumber}'
        ret = "=== GAME ===\n\t"
        ret += f"deck = {self.__deck}\n\t"
        ret += f"nTotal = {self.__nTotal}\n\t"
        ret += f"nPlayers = {self.__nPlayers}\n\t"
        ret += f"nBots = {self.__nBots}\n\t"
        ret += f"players = {self.__players}\n\t"
        ret += f"roles = {self.__roles}\n\t"
        ret += f"nHand = {self.__nHand}\n\t"
        ret += f"nSpare = {self.__nSpare}\n\t"
        ret += f"winners = {self.__winners}\n\t"
        ret += f"gameNumber = {self.__gameNumber}\n\t"
        ret += f"roundNumber = {self.__roundNumber}\n\t"
        ret += f"turnNumber = {self.__turnNumber}\n\t"
        ret += f"currPlayer = {self.__currPlayer}\n\t"
        ret += f"topMove = {self.__topMove}\n\t"
        return ret















    ### TERMINAL VERSION FUNCTION
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


    ### TERMINAL VERSION FUNCTION
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

                self.newGame()
                continue

            next_pid = self.nextTurnPlayer()
            if next_pid == 0:
                self.__currPlayer = self.topMove.pid
                self.newGame()
            else:
                self.__currPlayer = next_pid
                self.__turnNumber += 1







# if __name__ == "__main__":
#     print("\t=== President and Insects ===\n\t    --- By Noah Correa ---\n")

#     while True:
#         num = input("Enter number of total players (5-7): ")
#         try:
#             num = int(num)
#             if num < 5 or num > 7:
#                 print("Error: please enter a number between 5 and 7")
#                 continue
#             break
#         except ValueError:
#             print("Error: please enter a valid number")
#     print("\n\nLOADING...\n\n")
#     game = Game(1, num)


#     for p_id in game.players:
#         game.players[p_id].printHand()

#     game.players[7].addCardHand(Card(6, "6", "Clubs"))
#     game.players[7].addCardHand(Card(6, "6", "Spades"))
#     game.players[7].addCardHand(Card(6, "6", "Diamonds"))
#     game.players[7].addCardHand(Card(6, "6", "Hearts"))
#     game.players[7].printHand()
#     while True:
#         pInput = input("Which card do you want to add to your move? ")
#         if pInput == "pass":
#             game.players[7].passTurn()
#         elif pInput == "play":
#             game.players[7].playTurn()
#         elif pInput == "q":
#             quit()
#         elif pInput == "":
#             game.players[7].printHand()
#             game.players[7].printMove()
#         else:
#             pInput = int(pInput) - 1
#             game.players[7].addCardMove(pInput)
#             game.players[7].printHand()
#             game.players[7].printMove()
