'''
File:           Client.py
Author:         Noah Correa
Date:           09/9/21
Description:    Client for Presidents and Insects
'''

import sys
import time
import pygame
# from time import sleep
from typing import Union
from math import sin, cos, atan2, pi, sqrt
import socket
import json

from src.status import Status
from src.card import Card, CARD_W, CARD_H
from src.game import Game
from src.move import Move
from src.player import Player
from src.bot import Bot
from src.buttons import GREY, PlainText, TextButton, PlainImage, ImageButton, CardButton, TextInput, BG_COLOUR, BLACK, YELLOW, RED, N, H1, H2


# Find largest 16:9 resolution smaller than host
def find_resolution(w,h):
    resolutions = [(3840,2160), (2560,1440), (1920,1080), (1600,900), (1366,768), (1280,720), (1152,648), (1024,576)]
    for nw, nh in resolutions:
        if nw < w and nh < h:
            return nw, nh


# Initialise Pygame and global variables
pygame.init()
info = pygame.display.Info()
startW, startH = info.current_w, info.current_h
displayFlags = pygame.HWSURFACE | pygame.DOUBLEBUF
WINDOW = pygame.display.set_mode(find_resolution(startW, startH), flags=displayFlags)
WINDOW_W, WINDOW_H = pygame.display.get_window_size()
WINDOW.fill(BG_COLOUR)
pygame.display.set_caption("Presidents and Insects")
pygame.display.set_icon(pygame.image.load('resources/icons/cockroach.png').convert_alpha())
pygame.display.flip()

FRAMERATE = 120
SOCKET: socket.socket = None
USERNAME: str = None
BUFSIZE = 1024*2


#! Pygame Screens ------------------------------------------------------------------ #
#* Main menu screen
def game_intro():
    global WINDOW
    global WINDOW_W
    global WINDOW_H

    serverDisconnect()

    clock = pygame.time.Clock()
    run = True
    while run:
        tb_sp = TextButton('Singleplayer', 60, (WINDOW_W//2, 2*WINDOW_H//3), sp_number, align='c', font=H2)
        tb_mp = TextButton('Multiplayer', 60, (WINDOW_W//2, 2*WINDOW_H//3+60), mp_connect, align='c', font=H2)
        tb_settings = TextButton('Settings', 60, (WINDOW_W//2, 2*WINDOW_H//3+60*2), settings, align='c', font=H2)
        pt_pai = PlainText('Presidents and Insects', 100, (WINDOW_W//2,WINDOW_H//2), align='c', font=H1)
        pi_cockroach = PlainImage("resources/icons/cockroach.png", (151*2,191*2), (WINDOW_W//2,WINDOW_H//3-100), align='c')
        pos = pygame.mouse.get_pos()

        WINDOW.fill(BG_COLOUR)
        pi_cockroach.draw(WINDOW)
        pt_pai.draw(WINDOW)
        tb_settings.draw(WINDOW, pos)
        tb_sp.draw(WINDOW, pos)
        tb_mp.draw(WINDOW, pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.VIDEORESIZE:
                WINDOW_W, WINDOW_H = pygame.display.get_window_size()
            if event.type == pygame.MOUSEBUTTONDOWN:
                tb_settings.onClick(event)
                tb_sp.onClick(event)
                tb_mp.onClick(event)

        pygame.display.flip()
        clock.tick(FRAMERATE)


#* Settings screen
def settings():
    global WINDOW
    global WINDOW_W
    global WINDOW_H

    clock = pygame.time.Clock()
    run = True
    while run:
        tb_back = TextButton('Back', 50, (0, 0), None, font=H2)
        tb_mm = TextButton('Main Menu', 50, (WINDOW_W//2, WINDOW_H//2-90), game_intro, align='c')
        tb_fs = TextButton('Fullscreen', 50, (WINDOW_W//2,WINDOW_H//2-30), None, align='c')
        tb_quit = TextButton('Quit Game', 50, (WINDOW_W//2,WINDOW_H//2+30), quit_game, align='c')
        pos = pygame.mouse.get_pos()

        WINDOW.fill(BG_COLOUR)
        tb_back.draw(WINDOW, pos)
        tb_mm.draw(WINDOW, pos)
        tb_fs.draw(WINDOW, pos)
        tb_quit.draw(WINDOW, pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.VIDEORESIZE:
                WINDOW_W, WINDOW_H = pygame.display.get_window_size()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tb_fs.onClick(event):
                    pygame.display.toggle_fullscreen()
                    WINDOW_W, WINDOW_H = pygame.display.get_window_size()
                    pygame.time.delay(100)
                tb_mm.onClick(event)
                tb_quit.onClick(event)
                if tb_back.onClick(event):
                    return

        pygame.display.flip()
        clock.tick(FRAMERATE)


#* Rules screen - CURRENTLY UNUSED
def rules():
    global WINDOW
    global WINDOW_W
    global WINDOW_H

    clock = pygame.time.Clock()
    run = True
    while run:
        tb_back = TextButton('Back', 50, (0, 0), None, font=H2)
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.VIDEORESIZE:
                WINDOW_W, WINDOW_H = pygame.display.get_window_size()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tb_back.onClick(event):
                    return

        WINDOW.fill(BG_COLOUR)
        # TODO: Render rules
        tb_back.draw(WINDOW, pos)

        pygame.display.flip()
        clock.tick(FRAMERATE)


#* Singleplayer number of players screen
def sp_number():
    global WINDOW
    global WINDOW_W
    global WINDOW_H

    clock = pygame.time.Clock()
    run = True
    while run:
        tb_back = TextButton('Back', 50, (0, 0), game_intro, font=H2)
        tb_5 = TextButton('5', 100, (WINDOW_W//2-200,WINDOW_H//2), sp_loading, params=5)
        tb_6 = TextButton('6', 100, (WINDOW_W//2-50,WINDOW_H//2), sp_loading, params=6)
        tb_7 = TextButton('7', 100, (WINDOW_W//2+100,WINDOW_H//2), sp_loading, params=7)
        pt_numPlayers = PlainText('Choose total number of players', 50, (WINDOW_W//2,WINDOW_H//3), align='c', font=H2)
        pos = pygame.mouse.get_pos()

        WINDOW.fill(BG_COLOUR)
        pt_numPlayers.draw(WINDOW)
        tb_back.draw(WINDOW, pos)
        tb_5.draw(WINDOW, pos)
        tb_6.draw(WINDOW, pos)
        tb_7.draw(WINDOW, pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.VIDEORESIZE:
                WINDOW_W, WINDOW_H = pygame.display.get_window_size()
            if event.type == pygame.MOUSEBUTTONDOWN:
                tb_back.onClick(event)
                tb_5.onClick(event)
                tb_6.onClick(event)
                tb_7.onClick(event)

        pygame.display.flip()
        clock.tick(FRAMERATE)


#* Singleplayer loading screen
def sp_loading(total: int) -> None:
    global WINDOW
    global WINDOW_W
    global WINDOW_H
    WINDOW_W, WINDOW_H = pygame.display.get_window_size()
    sound_shuffleCards = pygame.mixer.Sound('resources/audio/card_shuffle.wav')
    sound_shuffleCards.set_volume(0.1)
    sound_shuffleCards.play()
    WINDOW.fill(BG_COLOUR)
    pt_loading = PlainText('LOADING', 50, (WINDOW_W//2,WINDOW_H//2), align='c')
    pt_loading.draw(WINDOW)
    pygame.display.flip()
    pygame.time.delay(500)
    game = Game()
    game.startSP(total)
    pygame.time.delay(500)
    sound_shuffleCards.stop()
    sp_game_loop(game)


#* Game screen
def sp_game_loop(game: Game) -> None:
    global WINDOW
    global WINDOW_W
    global WINDOW_H

    sound_playCard = pygame.mixer.Sound('resources/audio/play_card.wav')
    sound_playCard.set_volume(0.1)
    tb_settings = ImageButton('resources/icons/menu_icon.png', (50,50), (0,0), settings)
    tb_settings.setHover('resources/icons/menu_icon_hover.png')

    player: Player = game.getPlayer('Player 1')
    # ADDED BOT DELAY
    # 0 for delay, -1 for no delay
    botDelay = 0

    clock = pygame.time.Clock()
    run = True
    while run:
        # Draw all default stuff
        WINDOW.fill(BG_COLOUR)
        
        # Draw information at top of screen
        game_round_turn_text = PlainText(f"Game {game.gameNumber} Round {game.roundNumber} Turn {game.turnNumber}", 40, (WINDOW_W//2, 20), align='c', font=H2)
        game_round_turn_text.draw(WINDOW)
        tb_pass = TextButton('Pass', 50, (WINDOW_W-5, WINDOW_H), None, align='br')

        # Draw buttons
        pos = pygame.mouse.get_pos()
        tb_settings.draw(WINDOW, pos)

        # Draw player cards
        draw_player_cards(pos, player)

        # Draw other players cards
        pcpa = draw_other_cards(game, player)

        # Draw top move
        topMove: Move = game.topMove
        draw_top_pile(game.prevMoves, pcpa)
        nextTurn = False

        # Game logic
        # Get the current player
        currPlayer: Union[Player, Bot] = game.getCurrentPlayer()

        # Check if bot
        isValidMove = False
        if currPlayer.isBot:
            # Check bot move is valid

            isValidMove = None
            if botDelay == 40 or botDelay == -1:
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
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                if event.type == pygame.VIDEORESIZE:
                    WINDOW_W, WINDOW_H = pygame.display.get_window_size()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    tb_settings.onClick(event)

        else:
            botDelay = 0 if botDelay != -1 else -1
            # Draw Pygame

            p_hand, p_move = draw_player_cards(pos, currPlayer)

            tb_play = TextButton('Play', 50, (WINDOW_W//2+CARD_W*len(player.move)//2+CARD_W,WINDOW_H-CARD_H-CARD_H//4), None, align='c')
            if game.playerValidMove(player):
                tb_play.draw(WINDOW, pos)
            tb_pass.draw(WINDOW, pos)
            # Loop through events
            for event in pygame.event.get():
                # Check if game quit
                if event.type == pygame.QUIT:
                    quit_game()
                if event.type == pygame.VIDEORESIZE:
                    WINDOW_W, WINDOW_H = pygame.display.get_window_size()
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
            newRound = game.newTurn()
            if newRound:
                sound_shuffleCards = pygame.mixer.Sound('resources/audio/card_shuffle.wav')
                sound_shuffleCards.set_volume(0.1)
                sound_shuffleCards.play()
                pygame.time.delay(500)

        pygame.display.flip()
        clock.tick(FRAMERATE)


#* Multiplayer load screen
def mp_connect():
    global WINDOW
    global WINDOW_W
    global WINDOW_H
    global SOCKET
    global USERNAME

    # Reset socket and username if going back to mp screen
    SOCKET, USERNAME = None, None

    ti_name = TextInput((325, 40), (WINDOW_W//2,WINDOW_H//3+80), max_string_length=10)
    ti_server = TextInput((400, 40), (WINDOW_W//2,WINDOW_H//2+40), max_string_length=-1, initial_string="114.74.28.174:9229")

    ti_current = None
    connected = None
    connect_attempt = False
    clock = pygame.time.Clock()
    run = True
    while run:
        tb_connect = TextButton('Connect', 50, (WINDOW_W//2, WINDOW_H//2+110), None, align='c', font=H2)
        tb_back = TextButton('Back', 50, (0, 0), game_intro, font=H2)
        pt_name = PlainText('Enter your name:', 50, (WINDOW_W//2,WINDOW_H//3), align='c', font=H2)
        pt_len = PlainText('Max 10 characters', 30, (WINDOW_W//2,WINDOW_H//3+40), align='c', font=N)
        pt_server = PlainText('Enter server', 50, (WINDOW_W//2,WINDOW_H//2), align='c', font=H2)
        pt_error = PlainText('Unable to connect to server', 30, (WINDOW_W//2, WINDOW_H//2+160), align='c', font=N)
        
        pos = pygame.mouse.get_pos()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.VIDEORESIZE:
                WINDOW_W, WINDOW_H = pygame.display.get_window_size()
            if event.type == pygame.MOUSEBUTTONDOWN:
                tb_back.onClick(event)
                if tb_connect.onClick(event):
                    connect_attempt = True
                    connected = attempt_connect(ti_name.get_text(), ti_server.get_text())
                    # if connected is None:
                    #     # Display name taken message
                    #     pass
                if ti_name.onClick(event):
                    ti_current = 'name'
                if ti_server.onClick(event):
                    ti_current = 'server'

        if ti_current == 'name':
            ti_name.update(events)
        if ti_current == 'server':
            ti_server.update(events)

        if connected is not None:
            SOCKET, data = connected
            USERNAME = data.get('name')
            lobby_screen()
            return


        WINDOW.fill(BG_COLOUR)
        ti_name.draw(WINDOW)
        ti_server.draw(WINDOW)
        pt_name.draw(WINDOW)
        pt_len.draw(WINDOW)
        pt_server.draw(WINDOW)
        tb_connect.draw(WINDOW, pos)
        tb_back.draw(WINDOW, pos)
        if connected is None and connect_attempt:
            pt_error.draw(WINDOW, colour=RED)

        pygame.display.flip()
        clock.tick(FRAMERATE)


#* Multiplayer lobby screen
def lobby_screen():
    global WINDOW
    global WINDOW_W
    global WINDOW_H
    global SOCKET
    global USERNAME

    tb_settings = ImageButton('resources/icons/menu_icon.png', (50,50), (0,0), settings)
    tb_settings.setHover('resources/icons/menu_icon_hover.png')
    
    clock = pygame.time.Clock()
    run = True
    while run:
        pt_lobby = PlainText('Lobby', 50, (WINDOW_W//2, 25), align='c', font=H2)
        
        pos = pygame.mouse.get_pos()
        WINDOW.fill(BG_COLOUR)
        pt_lobby.draw(WINDOW)
        tb_settings.draw(WINDOW, pos)
        events = pygame.event.get()

        # Get the Lobby status
        try:
            data = sendrecvJSON(SOCKET, {'status': Status.LOBBY})
        except:
            continue
        code = data.get('status')
        if code == Status.LOBBY:
            players = data.get('playerlist')
            for i, name in enumerate(players):
                pt_player = PlainText(name, 40, (WINDOW_W//2, 130 + 50*i), align='c', font=N)
                pt_player.draw(WINDOW)
            # print(data.get('player'))
            if data.get('player') is not None:
                player = loadPlayer(data.get('player'))
                print(player)
                # time.sleep(10)
                mp_game_loop(player)
                return
        # # Check if game started
        # elif code == Status.PLAYER:
        #     print(data)

        elif code == Status.SHUTDOWN:
            print(f"Server shutdown or connection to server was lost")
            game_intro()
            return
        
        # Pygame event loop
        for event in events:
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.VIDEORESIZE:
                WINDOW_W, WINDOW_H = pygame.display.get_window_size()
            if event.type == pygame.MOUSEBUTTONDOWN:
                tb_settings.onClick(event)
        

        pygame.display.flip()
        clock.tick(FRAMERATE)



# Multiplayer game loop
def mp_game_loop(player: Player):
    global WINDOW
    global WINDOW_W
    global WINDOW_H
    global SOCKET
    global USERNAME

    SOCKET.settimeout(1)
    print("STARTED MP GAME LOOP")
    # time.sleep(10)
    sound_playCard = pygame.mixer.Sound('resources/audio/play_card.wav')
    sound_playCard.set_volume(0.1)
    tb_settings = ImageButton('resources/icons/menu_icon.png', (50,50), (0,0), settings)
    tb_settings.setHover('resources/icons/menu_icon_hover.png')
    


    # # Create player and set the hand
    # player: Player = game.getPlayer('Player 1')
    i = 0
    clock = pygame.time.Clock()
    run = True
    while run:
        print(f"looping {i}")
        i += 1
        WINDOW.fill(BG_COLOUR)
        tb_settings.draw(WINDOW)
        # print("sending GAME")
        # try:
        #     sendJSON(SOCKET, {'status': Status.GAME})
        #     data = recvJSON(SOCKET)
        try:
            data = sendrecvJSON(SOCKET, {'status': Status.GAME})
        except:
            print("nothing received")
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         quit_game()
            #     if event.type == pygame.VIDEORESIZE:
            #         WINDOW_W, WINDOW_H = pygame.display.get_window_size()
            #     if event.type == pygame.MOUSEBUTTONDOWN:
            #         tb_settings.onClick(event)
            continue
        # print(f"receiving {data.get('status')}")
        # except:
        #     continue
        # Draw all default stuff
        if data.get('game') == {}:
            print("empty game")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                if event.type == pygame.VIDEORESIZE:
                    WINDOW_W, WINDOW_H = pygame.display.get_window_size()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    tb_settings.onClick(event)
            continue
        else:
            game = data.get('game')

        
        game_info = f"Game {game.get('gameNumber')} Round {game.get('roundNumber')} Turn {game.get('turnNumber')}"
        game_round_turn_text = PlainText(game_info, 40, (WINDOW_W//2, 20), align='c', font=H2)
        game_round_turn_text.draw(WINDOW)
        tb_pass = TextButton('Pass', 50, (WINDOW_W-5, WINDOW_H), None, align='br')

        pos = pygame.mouse.get_pos()
        tb_settings.draw(WINDOW, pos)

        # Draw player cards
        currPlayerID = game.get('game')
        draw_player_cards(pos, player)

        # Draw other players cards
        # pcpa = draw_other_cards(game, player)

        # Draw top move
        # topMove: Move = game.topMove
        # draw_top_pile(game.prevMoves, pcpa)
        # events = pygame.event.get()
        # for event in events:
        #     if event.type == pygame.QUIT:
        #         quit_game()
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         tb_settings.onClick(event)


        # Game logic

        # # Check if not current player
        if currPlayerID != player.id:
            # Just handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                if event.type == pygame.VIDEORESIZE:
                    WINDOW_W, WINDOW_H = pygame.display.get_window_size()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    tb_settings.onClick(event)

        else:
            # Draw Pygame
            p_hand, p_move = draw_player_cards(pos, player)

            tb_play = TextButton('Play', 50, (WINDOW_W//2+CARD_W*len(player.move)//2+CARD_W,WINDOW_H-CARD_H-CARD_H//4), None, align='c')
            # if game.playerValidMove(player):
            #     tb_play.draw(WINDOW, pos)
            tb_pass.draw(WINDOW, pos)
            # Loop through events
            for event in pygame.event.get():
                # Check if game quit
                if event.type == pygame.QUIT:
                    quit_game()
                if event.type == pygame.VIDEORESIZE:
                    WINDOW_W, WINDOW_H = pygame.display.get_window_size()
                # Check if mouse clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if back button clicked
                    tb_settings.onClick(event)

                    playerMove = None
                    if tb_pass.onClick(event):
                        # TODO
                        playerMove = player.passTurn()
                    elif tb_play.onClick(event):
                        # TODO
                        playerMove = player.playTurn()


                    # if playerMove is not None:
                    #     isValidMove = game.validMove(playerMove)

                    #     if isValidMove:
                    #         game.addTopMove(playerMove)
                    #         if not playerMove.passed:
                    #             sound_playCard.play()
                    #         nextTurn = True
                    #     else:
                    #         currPlayer.addInvalidMove(playerMove)

                    # Check which card was clicked
                    for i, card in enumerate(p_hand):
                        if card.onClick(event):
                            sound_playCard.play()
                            player.addCardMove(i)

                    for i, card in enumerate(p_move):
                        if card.onClick(event):
                            sound_playCard.play()
                            player.addCardMoveHand(card.getCard())
        # # Check if its the next turn 
        # if nextTurn:
        #     # Check if the next turn starts a new round
        #     newRound = game.newTurn()
        #     if newRound:
        #         sound_shuffleCards = pygame.mixer.Sound('resources/audio/card_shuffle.wav')
        #         sound_shuffleCards.set_volume(0.1)
        #         sound_shuffleCards.play()
        #         pygame.time.delay(500)


        pygame.display.flip()
        clock.tick(FRAMERATE)








# TODO: Move to helper functions section

# Attempts to connect to the server address with the given name
def attempt_connect(name: str, server: str) -> tuple[socket.socket, dict]:
    # print(f"attempt connect name: {name}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    server = server.split(':')
    ADDR, PORT = server[0], int(server[1])
    try:
        sock.connect((ADDR,PORT))
        json_name = {'status': Status.CONNECT, 'name': name}
        data = sendrecvJSON(sock, json_name)

        if data.get('status') == Status.VALID:
            # print(data)
            print(f"'{data.get('name')}' connected")
            return sock, data
    except:
        print(f"Could not connect to server {server}")
        return None


# Loads a player into Player object
def loadPlayer(pdata: dict) -> Player:
    id = pdata.get('id')
    name = pdata.get('name')
    role = pdata.get('role')
    moveRank = pdata.get('moveRank')
    passed = pdata.get('passed')
    hand = []
    for cdata in pdata.get('hand'):
        rank = cdata.get('rank')
        value = cdata.get('value')
        suit = cdata.get('suit')
        kh = cdata.get('kingHearts')
        card = Card(rank, value, suit, kingHearts=kh)
        hand.append(card)
    move = []
    for cdata in pdata.get('move'):
        rank = cdata.get('rank')
        value = cdata.get('value')
        suit = cdata.get('suit')
        kh = cdata.get('kingHearts')
        card = Card(rank, value, suit, kingHearts=kh)
        move.append(card)

    player = Player(name, id=id, role=role, hand=hand, move=move, moveRank=moveRank, passed=passed)
    return player


# Send and Receive JSON data
def sendrecvJSON(sock:socket, data) -> dict:
    sendJSON(sock, data)
    while True:
        try:
            data = recvJSON(sock)
        except:
            continue
        break
    return data

# Receives socket data and converts from str to JSON (dict)
def recvJSON(sock: socket) -> dict:
    while True:
        try:
            data = json.loads(sock.recv(BUFSIZE).decode('utf-8'))
            break
        except:
            continue
    return data


# Sends socket data after converting from JSON (dict) to string
def sendJSON(sock: socket, data) -> None:
    # print(type(data), data)
    json_data = json.dumps(data, indent=4)
    # print(json_data)
    sock.send(json_data.encode('utf-8'))

# Disconnects from server
def serverDisconnect():
    global SOCKET
    global USERNAME
    if SOCKET is not None:
        json = {'status': Status.DISCONNECT, 'name': USERNAME}
        sendJSON(SOCKET, json)
        SOCKET, USERNAME = None, None






# ! Helper Funcitons ---------------------------------------------------------------- #

# Draw top pile card(s)
def draw_top_pile(top: list[Move], pcpa: dict) -> None:
    global WINDOW
    global WINDOW_W
    global WINDOW_H
    if len(top) == 0:
        return
    # x, y = WINDOW_W//2 - (CARD_W + CARD_W//2*(top.nCards-1))//2, WINDOW_H//2 - CARD_H//2
    # for i, card in enumerate(top.cards):
    #     WINDOW.blit(card.img, (x + CARD_W//2*i, y))
    cx, cy = WINDOW_W//2, WINDOW_H//2
    for i, move in enumerate(top):
        player_pcpa = pcpa.get(move.pid)
        if player_pcpa is None:
            player_pcpa = [0]
        angle = player_pcpa[0]
        mid = (CARD_W//8*(move.nCards-1)+CARD_W)//2 - CARD_W//2
        startx = cx - mid * cos(angle*pi/180)
        starty = cy + mid * sin(angle*pi/180)
        for j, card in enumerate(move.cards):
            pos = startx + j*(CARD_W//8*cos(angle*pi/180)), starty - j*(CARD_W//8*sin(angle*pi/180))
            image = pygame.transform.rotate(card.img, angle)
            rect = image.get_rect(center=pos)
            WINDOW.blit(image, rect)


# Draws both player hand and move cards
def draw_player_cards(pos, player: Player) -> tuple[list[CardButton], list[CardButton]]:
    pHand = draw_player_hand(pos, player)
    pMove = draw_player_move(pos, player)
    return pHand, pMove


# Draws the players hand on screen
def draw_player_hand(pos, player: Player) -> list[CardButton]:
    global WINDOW
    global WINDOW_W
    global WINDOW_H
    ret = []
    start = WINDOW_W//2 - CARD_W * len(player.hand)//2
    for i, card in enumerate(player.hand):
        card = CardButton(player.hand[i], (start+CARD_W*i,WINDOW_H-CARD_H//2))
        card.draw(WINDOW, pos)
        ret.append(card)
    return ret


# Draws the players selected move on screen
def draw_player_move(pos, player: Player) -> list[CardButton]:
    global WINDOW
    global WINDOW_W
    global WINDOW_H
    ret = []
    start = WINDOW_W//2 - CARD_W * len(player.move)//2
    for i, card in enumerate(player.move):
        card = CardButton(player.move[i], (start+CARD_W*i,WINDOW_H-CARD_H-CARD_H//4-CARD_H//2))
        card.draw(WINDOW, pos)
        ret.append(card)
    return ret


# Draw other players cards
def draw_other_cards(game: Game, player: Player) -> dict:
    global WINDOW
    global WINDOW_W
    global WINDOW_H
    colour = BLACK
    if player.id == game.currPlayer:
        colour = YELLOW
    elif player.passed:
        colour = GREY

    pt_pName = PlainText(player.name, 50, (5,WINDOW_H-50), align='bl')
    pt_pName.draw(WINDOW, colour)
    pt_pRole = PlainText(player.role, 50, (5,WINDOW_H), align='bl')
    pt_pRole.draw(WINDOW, colour)

    other_players: list[Player] = []
    for p in game.players.values():
        if p != player:
            other_players.append(p)

    card = game.deck.getCardBack()

    # rect = pygame.Rect((CARD_H//2, 80 + CARD_H//2), (WINDOW_W-CARD_H,  WINDOW_H//2-CARD_H//2-(80 + CARD_H//2)))
    pcpa = __playerCardsPosAngle(game, other_players)

    for i, p in enumerate(other_players):
        colour = BLACK
        if p.id == game.currPlayer:
            colour = YELLOW
        elif p.passed:
            colour = GREY

        angle, (startx,starty), (centerx,centery) = pcpa[p.id]
        # Pygame rotation defined as counter-clockwise rotation from the positive x-axis
        c = pygame.transform.rotate(card, angle)

        for j in range(p.nCards):
            # draw all player cards here
            pos = startx + j*(CARD_W//8*cos(angle*pi/180)), starty - j*(CARD_W//8*sin(angle*pi/180))
            crect = c.get_rect(center=pos)
            WINDOW.blit(c, crect)

        pt_playerName = PlainText(p.name, 25, (centerx,centery+CARD_H*1.05), align='c')
        pt_playerName.draw(WINDOW, colour)
        pt_playerRole = PlainText(p.role, 25, (centerx,centery+CARD_H*1.05+30), align='c')
        pt_playerRole.draw(WINDOW, colour)
    return pcpa

# Caculates the locations/angles for all players
def __playerCardsPosAngle(game: Game, players: list[Player]):
    global WINDOW_W
    global WINDOW_H
    pcpa = {}
    cp = WINDOW_W//2, WINDOW_H
    a = (WINDOW_W-2*CARD_H)//2
    b = WINDOW_H//2-(40+CARD_H//2)
    for i, p in enumerate(players):
        xpos = CARD_H + (WINDOW_W-2*CARD_H)//(len(players)-1)*i
        ypos = -b/a*sqrt(a**2-(xpos-WINDOW_W//2)**2)+WINDOW_H//2
        center_pos = xpos, ypos
        angle = 90 - atan2((cp[1]-ypos),(cp[0]-xpos))*180/pi
        mid = (CARD_W//8*(p.nCards-1)+CARD_W)//2 - CARD_W//2
        startx = center_pos[0] - mid * cos(angle*pi/180)
        starty = center_pos[1] + mid * sin(angle*pi/180)
        pcpa[p.id] = (angle, (startx,starty), (xpos,ypos))
    return pcpa

# Quit game
def quit_game():
    serverDisconnect()
    pygame.quit()
    sys.exit()
    # quit()


if __name__ == "__main__":
    game_intro()
    quit_game()
