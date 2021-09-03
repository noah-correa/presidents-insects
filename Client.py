"""
main.py for Presidents and Insects Python Card Game
Noah Correa
"""
import sys
import pygame
from time import sleep
from typing import Union

from src.card import Card, CARD_W, CARD_H
from src.game import Game
from src.move import Move
from src.player import Player
from src.bot import Bot
from src.buttons import TextButton, CardButton, ImageButton, PlainText, BG_COLOUR, BLACK, WHITE, YELLOW

pygame.init()

window = pygame.display.set_mode((1600, 900))
WINDOW_W, WINDOW_H = pygame.display.get_window_size()
window.fill(BG_COLOUR)
pygame.display.set_caption("Presidents and Insects")
pygame.display.set_icon(pygame.image.load('resources/icons/cockroach.png'))
pygame.display.update()



# Main menu screen
def game_intro():
    tb_sp = TextButton('Singleplayer', 60, (WINDOW_W//2, 2*WINDOW_H//3), singleplayer_number, align='c', font='H2')
    tb_mp = TextButton('Multiplayer', 60, (WINDOW_W//2, 2*WINDOW_H//3+60), None, align='c', font='H2')
    tb_settings = TextButton('Settings', 60, (WINDOW_W//2, 2*WINDOW_H//3+60*2), settings, align='c', font='H2')
    pt_pai = PlainText('Presidents and Insects', 100, (WINDOW_W//2,WINDOW_H//2), align='c', font='H1')
    main_image = pygame.transform.scale(pygame.image.load("resources/icons/cockroach.png"), (151*2, 191*2))

    run = True
    while run:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                tb_settings.onClick(event)
                tb_sp.onClick(event)

        window.fill(BG_COLOUR)
        window.blit(main_image, (WINDOW_W // 2 - 151, WINDOW_H // 3 - 275))
        pt_pai.draw(window)
        tb_settings.draw(window, pos)
        tb_sp.draw(window, pos)
        tb_mp.draw(window, pos)

        pygame.display.update()
        pygame.time.delay(15)


# Choose total number of players screen
def singleplayer_number():

    b_back = TextButton('Back', 50, (0, 0), game_intro)
    b_5 = TextButton('5', 100, (WINDOW_W//2-200,WINDOW_H//2), loading_screen, params=5)
    b_6 = TextButton('6', 100, (WINDOW_W//2-50,WINDOW_H//2), loading_screen, params=6)
    b_7 = TextButton('7', 100, (WINDOW_W//2+100,WINDOW_H//2), loading_screen, params=7)
    pt_numPlayers = PlainText('Choose total number of players', 50, (WINDOW_W//2,WINDOW_H//3), align='c', font='H2')

    run = True
    while run:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                b_back.onClick(event)
                b_5.onClick(event)
                b_6.onClick(event)
                b_7.onClick(event)

        window.fill(BG_COLOUR)
        pt_numPlayers.draw(window)

        b_back.draw(window, pos)
        b_5.draw(window, pos)
        b_6.draw(window, pos)
        b_7.draw(window, pos)

        pygame.display.update()
        pygame.time.delay(15)



def settings():
    b_back = TextButton('Back', 50, (0, 0), None)
    b_fs = TextButton('Toggle Fullscreen', 50, (WINDOW_W//2,WINDOW_H//2-30), None, align='c')
    b_quit = TextButton('Quit Game', 50, (WINDOW_W//2,WINDOW_H//2+30), quit_game, align='c')

    run = True
    screen = None
    while run:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b_fs.onClick(event):
                    pygame.display.toggle_fullscreen()
                    pygame.time.delay(100)
                b_quit.onClick(event)
                if b_back.onClick(event):
                    return

        window.fill(BG_COLOUR)
        b_back.draw(window, pos)
        b_fs.draw(window, pos)
        b_quit.draw(window, pos)

        pygame.display.update()
        pygame.time.delay(15)

    # run_screen(screen)


# Rules screen
def rules():
    b_back = TextButton('Back', 50, (0, 0), None)

    run = True
    while run:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b_back.onClick(event):
                    return

            # if event.type == pygame.MOUSEMOTION:
                # b_back.draw(pos)

        window.fill(BG_COLOUR)
        # TODO: Render rules
        b_back.draw(window, pos)

        pygame.display.update()
        pygame.time.delay(15)

    # run_screen(screen)



def loading_screen(total: int) -> None:
    window.fill(BG_COLOUR)
    pt_loading = PlainText('LOADING', 50, (WINDOW_W//2,WINDOW_H//2), align='c')
    pt_loading.draw(window)
    pygame.display.update()
    pygame.time.delay(500)
    game = Game(1, total)
    game.newGame()
    pygame.time.delay(500)
    game_loop(game)
    # run_screen((game_loop, game))



# Game screen
def game_loop(game: Game) -> None:
    sound_playCard = pygame.mixer.Sound('resources/audio/play_card.wav')
    sound_playCard.set_volume(0.1)
    b_settings = ImageButton('resources/icons/menu_icon.png', (50,50), (0,0), settings, hover='resources/icons/menu_icon_hover.png')
    b_play = TextButton('Play', 50, (WINDOW_W,WINDOW_H-110), None, align='br')
    b_pass = TextButton('Pass', 50, (WINDOW_W, WINDOW_H-50), None, align='br')

    # ADDED BOT DELAY
    # 0 for delay, -1 for no delay
    botDelay = 0

    run = True
    while run:
        # Draw all default stuff
        window.fill(BG_COLOUR)
        game_round_turn_text = PlainText(f"Game {game.gameNumber} Round {game.roundNumber} Turn {game.turnNumber}", 40, (WINDOW_W//2, 0), align='c')
        game_round_turn_text.draw(window)
        nCards_text = PlainText(game.getPlayersNumCards(), 40, (WINDOW_W//2, 60), align='c')
        nCards_text.draw(window)

        pos = pygame.mouse.get_pos()
        b_settings.draw(window, pos)
        b_play.draw(window, pos)
        b_pass.draw(window, pos)

        topMove: Move = game.topMove
        draw_top_pile(topMove)
        nextTurn = False

        # Game logic
        currPlayer: Union[Player, Bot] = game.getCurrentPlayer()
        currPlayerText = f"{currPlayer.name}'s turn"
        if not currPlayer.isBot:
            currPlayerText = "Your turn"
        cp_text = PlainText(currPlayerText, 40, (WINDOW_W//2, 30), align='c')
        cp_text.draw(window)

        # Check if bot
        isValidMove = False
        if currPlayer.isBot:
            # Check bot move is valid

            isValidMove = None
            if botDelay == 50 or botDelay == -1:
                botMove = currPlayer.botPlayTurn(topMove)
                isValidMove = game.validMove(botMove)
                botDelay = 0 if botDelay != -1 else -1

            if isValidMove is not None:
                if isValidMove:
                    game.addTopMove(botMove)
                    if not botMove.passed:
                        sound_playCard.play()
                    # Bot played valid move
                    nextTurn = True
                else:
                    # Bot played invalid move
                    print("ERROR: Bot move invalid")
                    print(f"Bot tried to play: {botMove}")

        else:
            botDelay = 0 if botDelay != -1 else -1
            # Draw Pygame
            p_hand, p_move = draw_player_cards(pos, currPlayer)
            # Loop through events
            for event in pygame.event.get():
                # Check if game quit
                if event.type == pygame.QUIT:
                    quit_game()

                # Check if mouse clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if back button clicked
                    b_settings.onClick(event)
                    
                    playerMove = None
                    if b_pass.onClick(event):
                        playerMove = currPlayer.passTurn()
                    elif b_play.onClick(event):
                        playerMove = currPlayer.playTurn()
                        
                    if playerMove is not None:
                        isValidMove = game.validMove(playerMove)

                        if isValidMove:
                            game.addTopMove(playerMove)
                            if not playerMove.passed:
                                sound_playCard.play()
                            nextTurn = True
                        else:
                            currPlayer.addInvalidMove(playerMove)

                    # Check which card was clicked
                    for i, card in enumerate(p_hand):
                        if card.onClick(event):
                            sound_playCard.play()
                            currPlayer.addCardMove(i)

                    for i, card in enumerate(p_move):
                        if card.onClick(event):
                            sound_playCard.play()
                            currPlayer.addCardMoveHand(card.getCard())

        if botDelay >= 0:
            botDelay += 1

        if nextTurn:
            game.nextTurn()

        pygame.display.update()
        pygame.time.delay(15)

    # run_screen(screen)


# Draw top pile card(s)
def draw_top_pile(top: Move):
    # print(top)
    if top.nCards == 0:
        return
    x, y = WINDOW_W//2 - (CARD_W + CARD_W//2*(top.nCards-1))//2, WINDOW_H//2 - CARD_H//2
    for i, card in enumerate(top.cards):
        window.blit(card.img, (x + CARD_W//2*i, y))

# Draws both player hand and move cards
def draw_player_cards(pos, player: Player) -> tuple[list[CardButton], list[CardButton]]:
    pHand = draw_player_hand(pos, player)
    pMove = draw_player_move(pos, player)
    return pHand, pMove


# Draws the players hand on screen
def draw_player_hand(pos, player: Player) -> list[CardButton]:
    ret = []
    start = WINDOW_W//2 - CARD_W * len(player.hand)//2
    for i, card in enumerate(player.hand):
        card = CardButton(player.hand[i], (start+CARD_W*i,WINDOW_H-CARD_H//2))
        card.draw(window, pos)
        ret.append(card)
    return ret

# Draws the players selected move on screen
def draw_player_move(pos, player: Player) -> list[CardButton]:
    ret = []
    start = WINDOW_W//2 - CARD_W * len(player.move)//2
    for i, card in enumerate(player.move):
        card = CardButton(player.move[i], (start+CARD_W*i,WINDOW_H-CARD_H-CARD_H//4-CARD_H//2))
        card.draw(window, pos)
        ret.append(card)
    return ret

# Quit game
def quit_game():
    pygame.display.quit()
    pygame.quit()
    sys.exit()
    # quit()

if __name__ == "__main__":
    game_intro()
    quit_game()
