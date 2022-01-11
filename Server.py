'''
File:           Server.py
Author:         Noah Correa
Date:           09/9/21
Description:    Runs a Presidents and Insects server
'''

import sys
import os
import time
import json
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, timeout, gethostname, gethostbyname
import urllib.request
import json
import threading
import msvcrt
import select
# import pygame

from src.game import Game
from src.player import Player
from src.status import Status


PLAYERS: dict = {}                  # holds active players in format { <username>: [<socket>, <address>], ...}
CONNECTED: dict = {}                # players connected (after game has started)
T_LOCK = threading.Condition()      # thread lock
GAME: Game = None
SHUTDOWN = False
STARTGAME = False
SOCKET: socket = None
BUFSIZE = 1024*2
# pygame.init()

def getIP():
    return json.loads(urllib.request.urlopen('https://jsonip.com/').read())['ip']

def start_server():
    global PLAYERS
    global T_LOCK
    global GAME
    global STARTGAME
    global SOCKET

    if len(sys.argv) == 1:
        ADDR = 'localhost'
        PORT = 9229
    elif len(sys.argv) == 2:
        ADDR = ''
        PORT = int(sys.argv[1])
    else:
        print("Usage: python Server.py <server port>")
        sys.exit()

    print(f"Starting server at {getIP()}:{PORT}")

    SOCKET = socket(AF_INET, SOCK_STREAM)
    SOCKET.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    SOCKET.bind((ADDR, PORT))
    SOCKET.listen(1)
    SOCKET.setblocking(False)

    GAME = Game(nopygame=True)

    print("ADMIN COMMANDS:\n\t- 'q': Quit the server\n\t- 's': Start a game")
    print("Waiting for players to join")
    while True:
        try:
            # Accept a client and create a thread for it
            playerSocket, playerAddress = SOCKET.accept()
            # print(f"{playerAddress} connected")
            threading.Thread(target=playerThread, args= (playerSocket, playerAddress)).start()

        except BlockingIOError:
            continue
        except OSError:
            break
        finally:
            # Handle server input
            if msvcrt.kbhit():
                c = msvcrt.getch().decode()
                # print(f"kbhit: {c}")
                if c == 'q':
                    quit_server()
                elif c == 's':
                    # Check enough players
                    if 5 <= len(list(PLAYERS.keys())) <= 7 and not STARTGAME:
                        with T_LOCK:
                            print("Starting game")
                            GAME.startMP()
                            # print(GAME)
                            STARTGAME = True
                            T_LOCK.notify()
                    else:
                        print("Cannot start game! Must have 5-7 players")
            time.sleep(0.1)
    SOCKET.close()


# THREADED FUNCTION
def playerThread(playerSocket: socket, playerAddress):
    global PLAYERS
    global T_LOCK
    global SHUTDOWN
    global GAME
    global STARTGAME
    global CONNECTED

    # playerSocket.setblocking(False)
    playerName = None
    
    # playerSocket.settimeout(1)
    # Handle player commands
    while True:
        if SHUTDOWN:
            return
        # Handle incoming client request
        with T_LOCK:
            try:
                # Receive command from client
                data = recvJSON(playerSocket)
                # print(f"receiving {data.get('status')}")

            except:
                T_LOCK.notify()
                continue
            
            if STARTGAME:
                print(f"RECEIVED: {data}")
            code = data.get('status')
            response = {}
            # Handle client responses
            
            # Client connect to server
            if code == Status.CONNECT:
                playerName = data.get('name')
                response = playerConnect(playerSocket, playerAddress, playerName)
                CONNECTED[playerName] = 0
            
            # Check if player disconnected from server
            elif code == Status.DISCONNECT:
                GAME.delPlayer(playerName)
                PLAYERS.pop(data['name'])
                CONNECTED[playerName] = -1
                print(f"'{playerName}' disconnected")
                print(f"PLAYER LIST ({len(PLAYERS)}): {list(PLAYERS.keys())}")
                return

            # Client is connected, requesting lobby list
            elif code == Status.LOBBY:
                # print(STARTGAME)
                if not STARTGAME:
                    response = {'status': Status.LOBBY, 'playerlist': list(PLAYERS.keys())}
                else:
                    response = {'status': Status.LOBBY, 'playerlist': list(PLAYERS.keys()), 'player': GAME.getPlayer(playerName).__dict__()}
                    # print(f"send '{playerName}': {response}")
                    # print(f"sending size {sys.getsizeof(response)}")

            elif code == Status.GAME:
                CONNECTED[playerName] = 1
                if not SHUTDOWN:
                    print(f"'{playerName}' has {sum(CONNECTED.values())}/{len(PLAYERS.keys())} connected")
                    if sum(CONNECTED.values()) == len(PLAYERS.keys()):
                        # All players connected
                        response = {'status': Status.GAME, 'game': GAME.__dict__()}
                    else:
                        response = {'status': Status.GAME, 'game': {}}
                else:
                    response = {'status': Status.SHUTDOWN}

            # Send response message back to client
            if STARTGAME: 
                print(f"sending {playerName}:\n{response}")
            sendJSON(playerSocket, response)
            # time.sleep(1)
            T_LOCK.notify()



def playerConnect(sock, addr, name):
    global PLAYERS
    
    # Player entered a name already active
    if PLAYERS.get(name) != None:
        json_status = {'status': Status.INVALID, 'errmsg': f"Player '{name}' already exists"}
        sendJSON(sock, json_status)

    # Player enters a new name
    else:
        # Send OK message
        validName = GAME.addNewPlayer(name)
        if not validName:
            json_status = {'status': Status.INVALID, 'errmsg': f"Player '{name}' is invalid (must be alphanumeric only)"}
        else:
            # playerObj = Player(name)
            # json_status = {'status': Status.VALID, 'player': playerObj.__dict__()}
            json_status = {'status': Status.VALID, 'name': name}
            # Add player to active players
            PLAYERS[name] = [sock, addr]
            print(f"  -> {name} logged into server from {addr[0]}:{addr[1]}")
            print(f"PLAYER LIST ({len(PLAYERS)}): {list(PLAYERS.keys())}")

    return json_status


# # Starts the game
# def start_game():
#     global GAME
#     global PLAYERS
#     global STARTGAME
#     global T_LOCK
#     global SHUTDOWN

#     print("Starting game")
#     with T_LOCK:
#         GAME.startMP()
#         time.sleep(4.5)
#         STARTGAME = True
#         T_LOCK.notify()
    # with T_LOCK:
    #     for player in GAME.players.values():
    #         json_data = {'status': Status.PLAYER, 'player': player.__dict__()}
    #         print(f"Sent player '{player.name}':\n{json_data}")
    #         sendPlayerJSON(player.name, json_data)
    #     T_LOCK.notify()
    # while True:
    #     if SHUTDOWN:
    #         quit_server()
    #     with T_LOCK:
    #         T_LOCK.notify()
    


# Quits the server
def quit_server():
    global PLAYERS
    global GAME
    global SHUTDOWN
    global T_LOCK
    global SOCKET
    if not STARTGAME:
        with T_LOCK:
            json = {'status': Status.SHUTDOWN}
            for sock, _ in PLAYERS.values():
                sendJSON(sock, json)
            T_LOCK.notify()
    SHUTDOWN = True
    SOCKET.close()
    sys.exit()


# Sends information to specific player
def sendPlayerJSON(name: str, data: dict) -> None:
    global PLAYERS
    global T_LOCK

    with T_LOCK:
        sock, _ = PLAYERS.get(name)
        if sock is not None:
            sendJSON(sock, data)
        T_LOCK.notify()

# Sends information to all players:
def sendAllJSON(data) -> None:
    global PLAYERS
    global T_LOCK
    with T_LOCK:
        for sock, _ in PLAYERS.values():
            sendJSON(sock, data)
        T_LOCK.notify()


def recvJSON(sock: socket) -> dict:
    while True:
        try:
            data = json.loads(sock.recv(BUFSIZE).decode('utf-8'))
            break
        except:
            continue
    return data

def sendJSON(sock: socket, data: dict) -> None:
    while True:
        try:
            # print(type(data), data)
            json_data = json.dumps(data, indent=4)
            # print(json_data)
            sock.send(json_data.encode('utf-8'))
            break
        except:
            continue



if __name__ == "__main__":
    start_server()
    quit_server()