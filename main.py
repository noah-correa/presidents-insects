"""
main.py for Presidents and Insects Python Card Game
Noah Correa
"""
import sys
import pygame
from time import sleep

from game import Game
from move import Move
from player import Player
from bot import Bot
from buttons import WINDOW_H, WINDOW_W, BG_COLOUR, Button, load_text, text_objects, BLACK, CardButton, PlainText



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

    run = True
    while run:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b_play.isOver(pos):
                    singleplayer_number()
                    run = False
                if b_rules.isOver(pos):
                    rules()
                    run = False
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
                    run = False
                    game_intro()
                if b_5.isOver(pos):
                    run = False
                    loading_screen(5)
                if b_6.isOver(pos):
                    run = False
                    loading_screen(6)
                if b_7.isOver(pos):
                    run = False
                    loading_screen(7)
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
                    run = False
                    game_intro()

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
    b_play = Button(window, WINDOW_W - 100, WINDOW_H - 110, 50, 'Play')
    b_pass = Button(window, WINDOW_W - 100, WINDOW_H - 50, 50, 'Pass')

    
    run = True
    while run:
        # Draw all default stuff
        window.fill(BG_COLOUR)
        game_round_turn_text = PlainText(window, WINDOW_W//2, 0, 40, f"Game {game.gameNumber} Round {game.roundNumber} Turn {game.turnNumber}", center=True)
        game_round_turn_text.draw()
        nCards_text = PlainText(window, WINDOW_W//2, 60, 40, game.getPlayersNumCards(), center=True)
        nCards_text.draw()

        pos = pygame.mouse.get_pos()
        b_back.draw(pos)
        b_play.draw(pos)
        b_pass.draw(pos)

        topMove: Move = game.topMove
        draw_top_pile(topMove)
        nextTurn = False

        # Game logic
        currPlayer: Player = game.getCurrentPlayer()
        currPlayerText = f"{currPlayer.name}'s turn"
        if not currPlayer.isBot:
            currPlayerText = "Your turn"
        cp_text = PlainText(window, WINDOW_W//2, 30, 40, currPlayerText, center=True)
        cp_text.draw()



        # Check if bot
        isValidMove = False
        if currPlayer.isBot:
            # Check bot move is valid
            botMove = currPlayer.botPlayTurn(topMove)
            isValidMove = game.validMove(botMove)
            if isValidMove:
                game.addTopMove(botMove)
                # Bot played valid move
                nextTurn = True
            else:
                # Bot played invalid move
                print("ERROR: Bot move invalid")
                print(f"Bot tried to play: {botMove}")

        else:
            # Draw Pygame
            p_hand, p_move = draw_player_cards(pos, currPlayer)
            # Loop through events
            for event in pygame.event.get():
                # Check if game quit
                if event.type == pygame.QUIT:
                    run = False

                # Check if mouse clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if back button clicked
                    if b_back.isOver(pos):
                        run = False
                        game_intro()
                        break
                    
                    playerMove = None
                    if b_pass.isOver(pos):
                        playerMove = currPlayer.passTurn()
                    elif b_play.isOver(pos):
                        playerMove = currPlayer.playTurn()
                        
                    if playerMove is not None:
                        isValidMove = game.validMove(playerMove)

                        if isValidMove:
                            game.addTopMove(playerMove)
                            nextTurn = True
                        else:
                            currPlayer.addInvalidMove(playerMove)

                    # Check which card was clicked
                    for i, card in enumerate(p_hand):
                        if card.isOver(pos):
                            currPlayer.addCardMove(i)

                    for i, card in enumerate(p_move):
                        if card.isOver(pos):
                            currPlayer.addCardMoveHand(card.getCard())

                # Check if cards are hovered
                # if event.type == pygame.MOUSEMOTION:
                #     b_back.draw(pos)
                    # draw_player_cards(pos, currPlayer)
                    # Check which card cursor is over
                    # for i, card in enumerate(p_hand):
                    #     if card.isOver(pos):
                    #         draw_player_cards(pos, currPlayer)

        if nextTurn:
            game.nextTurn()

        pygame.display.update()
        pygame.time.delay(15)

    quit_game()


# Draw top pile card(s)
def draw_top_pile(top: Move):
    # print(top)
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
