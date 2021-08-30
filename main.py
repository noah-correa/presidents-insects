"""
main.py for Presidents and Insects Python Card Game
Noah Correa
"""
import sys
import pygame

from game import Game
from move import Move
from player import Player
from bot import Bot
from buttons import WINDOW_H, WINDOW_W, BG_COLOUR, Button, load_text, text_objects, BLACK, CardButton



pygame.init()

window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
# print(type(window))
window.fill(BG_COLOUR)
pygame.display.set_caption("Presidents and Insects")
pygame.display.set_icon(pygame.image.load('images/cockroach.png'))
pygame.display.update()


# Main menu screen
def game_intro():

    b_play = Button(window, WINDOW_W//2-300, 2*WINDOW_H//3, 100, 'Play')
    b_rules = Button(window, WINDOW_W//2+100, 2*WINDOW_H//3, 100, 'Rules')

    # run = True
    while True:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b_play.isOver(pos):
                    singleplayer_number()
                    # run = False
                if b_rules.isOver(pos):
                    rules()
                    # run = False
            if event.type == pygame.MOUSEMOTION:
                b_play.draw(pos)
                b_rules.draw(pos)


        window.fill(BG_COLOUR)
        text = load_text(100)
        title, title_rect = text_objects("Presidents and Insects", text, BLACK)
        title_rect.center = ((WINDOW_W // 2), (WINDOW_H // 2))
        window.blit(title, title_rect)

        main_image = pygame.transform.scale(pygame.image.load("images/cockroach.png"), (151*2, 191*2))
        window.blit(main_image, (WINDOW_W // 2 - 151, WINDOW_H // 3 - 275))

        b_play.draw(pos)
        b_rules.draw(pos)

        pygame.display.update()
        pygame.time.delay(15)

    quit_game()

# Choose total number of players screen
def singleplayer_number():

    b_back = Button(window, 0, 0, 50, 'Back')
    b_5 = Button(window, WINDOW_W // 2 - 200, WINDOW_H // 2, 100, '5')
    b_6 = Button(window, WINDOW_W // 2 - 50, WINDOW_H // 2, 100, '6')
    b_7 = Button(window, WINDOW_W // 2 + 100, WINDOW_H // 2, 100, '7')

    run = True
    while run:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b_back.isOver(pos):
                    game_intro()
                    run = False
                if b_5.isOver(pos):
                    loading_screen(5)
                    run = False
                if b_6.isOver(pos):
                    loading_screen(6)
                    run = False
                if b_7.isOver(pos):
                    loading_screen(7)
                    run = False
            if event.type == pygame.MOUSEMOTION:
                b_back.draw(pos)
                b_5.draw(pos)
                b_6.draw(pos)
                b_7.draw(pos)

        window.fill(BG_COLOUR)

        text = load_text(50)
        title, title_rect = text_objects("Choose total number of players", text, BLACK)
        title_rect.center = ((WINDOW_W // 2), (WINDOW_H // 3))
        window.blit(title, title_rect)

        b_back.draw(pos)
        b_5.draw(pos)
        b_6.draw(pos)
        b_7.draw(pos)

        pygame.display.update()
        pygame.time.delay(15)

    quit_game()

# Rules screen
def rules():

    b_back = Button(window, 0, 0, 50, 'Back')

    run = True
    while run:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b_back.isOver(pos):
                    game_intro()
                    run = False

            if event.type == pygame.MOUSEMOTION:
                b_back.draw(pos)

        window.fill(BG_COLOUR)
        # TODO: Render rules
        b_back.draw(pos)

        pygame.display.update()
        pygame.time.delay(15)

    quit_game()


def loading_screen(total: int) -> None:
    window.fill(BG_COLOUR)
    text = load_text(50)
    title, title_rect = text_objects("LOADING", text, BLACK)
    title_rect.center = ((WINDOW_W // 2), (WINDOW_H // 3))
    window.blit(title, title_rect)
    pygame.display.update()
    pygame.time.delay(500)
    game = Game(1, total)
    game.newGame()
    pygame.time.delay(500)
    game_loop(game)

# Game screen
def game_loop(game: Game) -> None:
    b_back = Button(window, 0, 0, 50, 'Back')
    # run = True
    while True:
        window.fill(BG_COLOUR)
        # currPlayer = game.currPlayer

        # isValidMove = 0
        # if isinstance(self.players[self.currPlayer], Bot):
        #     botMove = self.players[self.currPlayer].botPlayTurn(self.topMove)
        #     isValidMove = self.validMove(botMove)
        #     if isValidMove:
        #         self.addTopMove(botMove)
        #         # Bot played valid move
        #     else:
        #         # Bot played invalid move

        # else:
        #     while True:
        #         playerMove = self.getUserInput()
        #         isValidMove = self.validMove(playerMove)
        #         if isValidMove:
        #             break
        #         print("\nMove invalid, please try again...\n")
        #         self.players[self.currPlayer].addInvalidMove(playerMove)
        #     self.addTopMove(playerMove)
        #     print(f"Player has {self.players[self.currPlayer].nCards} cards left after playing:\n\t" + str(playerMove))

        # if self.players[self.currPlayer].nCards == 0:
        #     print(f"==> {self.players[self.currPlayer].name} is now out in winners = {self.winners}")
        #     self.winners.append(self.currPlayer)
        # if len(self.winners) == self.nTotal - 1:
        #     self.__updatePlayerRole()
        #     self.__updateRoles()
        #     self.newGame()
        #     continue

        # next_pid = self.nextTurnPlayer()
        # if next_pid == 0:
        #     self.__currPlayer = self.topMove.pid
        #     self.newRound()
        # else:
        #     self.__currPlayer = next_pid
        #     self.__turnNumber += 1





        pos = pygame.mouse.get_pos()
        b_back.draw(pos)
        player = game.players[game.getPlayerId("Player 1")]
        p_hand, p_move = draw_player_cards(pos, player)
        # Loop through events
        for event in pygame.event.get():
            # Check if game quit
            if event.type == pygame.QUIT:
                quit_game()

            # Check if mouse clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if back button clicked
                if b_back.isOver(pos):
                    game_intro()
                    # run = False
                    break

                # Check which card was clicked
                for i, card in enumerate(p_hand):
                    if card.isOver(pos):
                        player.addCardMove(i)
                        draw_player_cards(pos, player)
                for i, card in enumerate(p_move):
                    if card.isOver(pos):
                        # print(card)
                        # print(card.getCard())
                        player.addCardMoveHand(card.getCard())
                        draw_player_cards(pos, player)

            # Check if cards are hovered
            if event.type == pygame.MOUSEMOTION:
                b_back.draw(pos)
                draw_player_cards(pos, player)
                # Check which card cursor is over
                for i, card in enumerate(p_hand):
                    if card.isOver(pos):
                        draw_player_cards(pos, player)

        pygame.display.update()
        pygame.time.delay(15)

    # quit_game()


# Draw top pile card(s)
def draw_top_pile(top: Move):
    if top.nCards == 0:
        return
    x, y = WINDOW_W//2 - 115//2*top.nCards, WINDOW_H//2 - 176//2
    for i, card in enumerate(top.cards):
        window.blit(card.img, (x + 115//2*i, y))

# Draws both player hand and move cards
def draw_player_cards(pos, player: Player) -> tuple(([CardButton], [CardButton])):
    pHand = draw_player_hand(pos, player)
    pMove = draw_player_move(pos, player)
    return pHand, pMove


# Draws the players hand on screen
def draw_player_hand(pos, player: Player) -> [CardButton]:
    ret = []
    start = WINDOW_W//2 - 115 * len(player.hand)//2
    for i, card in enumerate(player.hand):
        card = CardButton(window, player.hand[i], start + 115 * i, WINDOW_H - 176//2)
        card.draw(pos)
        ret.append(card)
    return ret

# Draws the players selected move on screen
def draw_player_move(pos, player: Player) -> [CardButton]:
    ret = []
    start = WINDOW_W//2 - 115 * len(player.move)//2
    for i, card in enumerate(player.move):
        card = CardButton(window, player.move[i], start + 115 * i, WINDOW_H - 176 - 176//4 - 176//2)
        card.draw(pos)
        ret.append(card)
    return ret

# Quit game
def quit_game():
    pygame.quit()
    sys.exit()
    # quit()

if __name__ == "__main__":
    game_intro()
    quit_game()
