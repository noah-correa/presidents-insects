"""
main.py for Presidents and Insects Python Card Game
Noah Correa
"""
import sys
import pygame
from time import sleep
from typing import Text, Union
from math import sin, cos, atan2, pi, sqrt

from src.card import Card, CARD_W, CARD_H
from src.game import Game
from src.move import Move
from src.player import Player
from src.bot import Bot
from src.buttons import PlainText, TextButton, PlainImage, ImageButton, CardButton, ImageAnimation, BG_COLOUR, N, H1, H2


pygame.init()
WINDOW = pygame.display.set_mode((1600, 900))
WINDOW_W, WINDOW_H = pygame.display.get_window_size()
WINDOW.fill(BG_COLOUR)
pygame.display.set_caption("Presidents and Insects")
pygame.display.set_icon(pygame.image.load('resources/icons/cockroach.png'))
pygame.display.update()



# Main menu screen
def game_intro():
    tb_sp = TextButton('Singleplayer', 60, (WINDOW_W//2, 2*WINDOW_H//3), sp_number, align='c', font=H2)
    tb_mp = TextButton('Multiplayer', 60, (WINDOW_W//2, 2*WINDOW_H//3+60), None, align='c', font=H2)
    tb_settings = TextButton('Settings', 60, (WINDOW_W//2, 2*WINDOW_H//3+60*2), settings, align='c', font=H2)
    pt_pai = PlainText('Presidents and Insects', 100, (WINDOW_W//2,WINDOW_H//2), align='c', font=H1)
    pi_cockroach = PlainImage("resources/icons/cockroach.png", (151*2,191*2), (WINDOW_W//2,WINDOW_H//3-100), align='c')
    # pi_cockroach = PlainImage("resources/icons/cockroach.png", (151*2,191*2), (WINDOW_W//2-151,WINDOW_H//3-275))

    run = True
    while run:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                tb_settings.onClick(event)
                tb_sp.onClick(event)

        WINDOW.fill(BG_COLOUR)
        pi_cockroach.draw(WINDOW)
        pt_pai.draw(WINDOW)
        tb_settings.draw(WINDOW, pos)
        tb_sp.draw(WINDOW, pos)
        tb_mp.draw(WINDOW, pos)

        pygame.display.update()
        pygame.time.delay(15)


# Settings screen
def settings():
    tb_back = TextButton('Back', 50, (0, 0), None)
    tb_mm = TextButton('Main Menu', 50, (WINDOW_W//2, WINDOW_H//2-90), game_intro, align='c')
    tb_fs = TextButton('Fullscreen', 50, (WINDOW_W//2,WINDOW_H//2-30), None, align='c')
    tb_quit = TextButton('Quit Game', 50, (WINDOW_W//2,WINDOW_H//2+30), quit_game, align='c')

    run = True
    screen = None
    while run:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tb_fs.onClick(event):
                    pygame.display.toggle_fullscreen()
                    pygame.time.delay(100)
                tb_mm.onClick(event)
                tb_quit.onClick(event)
                if tb_back.onClick(event):
                    return

        WINDOW.fill(BG_COLOUR)
        tb_back.draw(WINDOW, pos)
        tb_mm.draw(WINDOW, pos)
        tb_fs.draw(WINDOW, pos)
        tb_quit.draw(WINDOW, pos)

        pygame.display.update()
        pygame.time.delay(15)


# Rules screen
def rules():
    tb_back = TextButton('Back', 50, (0, 0), None)

    run = True
    while run:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tb_back.onClick(event):
                    return

        WINDOW.fill(BG_COLOUR)
        # TODO: Render rules
        tb_back.draw(WINDOW, pos)

        pygame.display.update()
        pygame.time.delay(15)



# Singleplayer number of players screen
def sp_number():
    tb_back = TextButton('Back', 50, (0, 0), game_intro)
    tb_5 = TextButton('5', 100, (WINDOW_W//2-200,WINDOW_H//2), sp_loading, params=5)
    tb_6 = TextButton('6', 100, (WINDOW_W//2-50,WINDOW_H//2), sp_loading, params=6)
    tb_7 = TextButton('7', 100, (WINDOW_W//2+100,WINDOW_H//2), sp_loading, params=7)
    pt_numPlayers = PlainText('Choose total number of players', 50, (WINDOW_W//2,WINDOW_H//3), align='c', font=H2)

    run = True
    while run:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                tb_back.onClick(event)
                tb_5.onClick(event)
                tb_6.onClick(event)
                tb_7.onClick(event)

        WINDOW.fill(BG_COLOUR)
        pt_numPlayers.draw(WINDOW)

        tb_back.draw(WINDOW, pos)
        tb_5.draw(WINDOW, pos)
        tb_6.draw(WINDOW, pos)
        tb_7.draw(WINDOW, pos)

        pygame.display.update()
        pygame.time.delay(15)


# Singleplayer loading screen
def sp_loading(total: int) -> None:
    WINDOW.fill(BG_COLOUR)
    pt_loading = PlainText('LOADING', 50, (WINDOW_W//2,WINDOW_H//2), align='c')
    pt_loading.draw(WINDOW)
    pygame.display.update()
    pygame.time.delay(500)
    game = Game()
    game.startSP(total)
    pygame.time.delay(500)
    sp_game_loop(game)


# Game screen
def sp_game_loop(game: Game) -> None:
    sound_playCard = pygame.mixer.Sound('resources/audio/play_card.wav')
    sound_playCard.set_volume(0.1)
    tb_settings = ImageButton('resources/icons/menu_icon.png', (50,50), (0,0), settings)
    tb_settings.setHover('resources/icons/menu_icon_hover.png')
    tb_play = TextButton('Play', 50, (WINDOW_W,WINDOW_H-50), None, align='br')
    tb_pass = TextButton('Pass', 50, (WINDOW_W, WINDOW_H), None, align='br')

    player: Player = game.getPlayer('Player 1')
    # ADDED BOT DELAY
    # 0 for delay, -1 for no delay
    botDelay = -1

    run = True
    while run:
        # Draw all default stuff
        WINDOW.fill(BG_COLOUR)
        
        # Draw information at top of screen
        game_round_turn_text = PlainText(f"Game {game.gameNumber} Round {game.roundNumber} Turn {game.turnNumber}", 40, (WINDOW_W//2, 20), align='c', font=H2)
        game_round_turn_text.draw(WINDOW)

        # nCards_text = PlainText(game.getPlayersNumCards(), 25, (WINDOW_W//2, 80), align='c')
        # nCards_text.draw(WINDOW)

        # Draw buttons
        pos = pygame.mouse.get_pos()
        tb_settings.draw(WINDOW, pos)
        tb_play.draw(WINDOW, pos)
        tb_pass.draw(WINDOW, pos)
        
        # Draw player cards
        draw_player_cards(pos, player)

        # Draw other players cards
        draw_other_cards(game, player)

        # Draw top move
        topMove: Move = game.topMove
        draw_top_pile(topMove)
        nextTurn = False

        # Game logic
        # Get the current player
        currPlayer: Union[Player, Bot] = game.getCurrentPlayer()
        currPlayerText = f"{currPlayer.name}'s turn"
        if not currPlayer.isBot:
            currPlayerText = "Your turn"
        cp_text = PlainText(currPlayerText, 40, (WINDOW_W//2, 55), align='c')
        cp_text.draw(WINDOW)

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
                    tb_settings.onClick(event)
                    
                    playerMove = None
                    if tb_pass.onClick(event):
                        playerMove = currPlayer.passTurn()
                    elif tb_play.onClick(event):
                        playerMove = currPlayer.playTurn()
                        
                    if playerMove is not None:
                        isValidMove = game.validMove(playerMove)
                        # print(isValidMove)

                        if isValidMove:
                            game.addTopMove(playerMove)
                            if not playerMove.passed:
                                sound_playCard.play()
                                # ia_moveCards = ImageAnimation(player.move[0], )
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


# Draw top pile card(s)
def draw_top_pile(top: Move):
    if top.nCards == 0:
        return
    x, y = WINDOW_W//2 - (CARD_W + CARD_W//2*(top.nCards-1))//2, WINDOW_H//2 - CARD_H//2
    for i, card in enumerate(top.cards):
        WINDOW.blit(card.img, (x + CARD_W//2*i, y))


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
        card.draw(WINDOW, pos)
        ret.append(card)
    return ret


# Draws the players selected move on screen
def draw_player_move(pos, player: Player) -> list[CardButton]:
    ret = []
    start = WINDOW_W//2 - CARD_W * len(player.move)//2
    for i, card in enumerate(player.move):
        card = CardButton(player.move[i], (start+CARD_W*i,WINDOW_H-CARD_H-CARD_H//4-CARD_H//2))
        card.draw(WINDOW, pos)
        ret.append(card)
    return ret


# Draw other players cards
def draw_other_cards(game: Game, player: Player):
    other_players: list[Player] = []
    for p in game.players.values():
        if p != player:
            other_players.append(p)

    # angle = 180//(len(other_players)-1)
    # start_angle = 90
    card = game.deck.getCardBack()
    cp = WINDOW_W//2, WINDOW_H

    # rect = pygame.Rect((CARD_H//2, 80 + CARD_H//2), (WINDOW_W-CARD_H,  WINDOW_H//2-CARD_H//2-(80 + CARD_H//2)))
    # pygame.draw.rect(WINDOW, (255,0,0), rect, width=5)

    # Other player card centers
    # Width
    a = (WINDOW_W-2*CARD_H)//2
    # Height
    b = WINDOW_H//2-(80+CARD_H//2)

    # print(a, b)

    for i, p in enumerate(other_players):
        xpos = CARD_H + (WINDOW_W-2*CARD_H)//(len(other_players)-1)*i
        ypos = -b/a*sqrt(a**2-(xpos-WINDOW_W//2)**2)+WINDOW_H//2
        # print(xpos)
        # print(WINDOW_H//2 - CARD_H - 20)
        # print(20+CARD_H)
        center_pos = xpos, ypos
        # print(center_pos)

        # Pygame rotation defined as counter-clockwise rotation from the positive x-axis
        angle = 90 - atan2((cp[1]-center_pos[1]),(cp[0]-center_pos[0]))*180/pi
        c = pygame.transform.rotate(card, angle)
        # print(f"Bot {i+1} angle={angle}")

        # angle = angle - 180
        # WINDOW_W//2 - (CARD_W + CARD_W//2*(top.nCards-1))//2
        mid = (CARD_W//8*(player.nCards-1)+CARD_W)//2 - CARD_W//2
        startx = center_pos[0] - mid * cos(angle*pi/180)
        starty = center_pos[1] + mid * sin(angle*pi/180)
        
        for j in range(p.nCards):
            # draw all player cards here
            pos = startx + j*(CARD_W//8*cos(angle*pi/180)), starty - j*(CARD_W//8*sin(angle*pi/180))
            crect = c.get_rect(center=pos)
            WINDOW.blit(c, crect)
            # pygame.draw.circle(WINDOW, (0,0,0), pos, 5)

        # crect = c.get_rect(center=center_pos)
        # WINDOW.blit(c, crect)
        # pygame.draw.circle(WINDOW, (0,0,255), center_pos, 5)
        # pygame.draw.circle(WINDOW, (0,255,255), (startx,starty), 5)
        # pygame.draw.line(WINDOW, (255,0,0), (xpos-mid,ypos), (xpos+mid,ypos), width=3)
        pt_playerName = PlainText(p.name, 25, (center_pos[0],center_pos[1]+CARD_H*1.05), align='c')
        pt_playerName.draw(WINDOW)
        pt_playerRole = PlainText(p.role, 25, (center_pos[0],center_pos[1]+CARD_H*1.05+30), align='c')
        pt_playerRole.draw(WINDOW)

    return


# Quit game
def quit_game():
    pygame.quit()
    sys.exit()
    # quit()


if __name__ == "__main__":
    game_intro()
    quit_game()
