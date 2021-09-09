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


PLAYERS = {}                        # holds active players in format { <username>: [<socket>, <address>, <Player>], ...}
T_LOCK = threading.Condition()      # thread lock
GAME = None
SHUTDOWN = False
# pygame.init()


class CmdThread(threading.Thread):
    def __init__(self, input_cbk = None, name='cl-input-thread'):
        self.input_cbk = input_cbk
        super(CmdThread, self).__init__(name=name)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            self.input_cbk(input()) #waits to get input + Return



def getIP():
    return json.loads(urllib.request.urlopen('https://jsonip.com/').read())['ip']

def start_server():
    global PLAYERS
    global T_LOCK
    global GAME

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
            print(f"{playerAddress} connected")
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
                    if 5 <= len(list(PLAYERS.keys())) <= 7:
                        start_game()
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

    # playerSocket.setblocking(False)
    playerName = None
    
    # Handle player commands
    while True:
        # Handle incoming client request
        with T_LOCK:
            if SHUTDOWN:
                return
            try:
                # Receive command from client
                data = recvJSON(playerSocket)
            except:
                T_LOCK.notify()
                continue

            # print(f"RECEIVED: {data}")
            code = data.get('status')
            response = {}
            # Handle client responses
            
            # Client connect to server
            if code == Status.CONNECT:
                playerName = data.get('name')
                response = playerConnect(playerSocket, playerAddress, playerName)
            
            # Check if player disconnected from server
            elif code == Status.DISCONNECT:
                GAME.delPlayer(playerName)
                PLAYERS.pop(data['name'])
                print(f"'{playerName}' disconnected")
                print(f"{len(PLAYERS)} total players {list(PLAYERS.keys())}")
                return

            # Client is connected, requesting lobby list
            elif code == Status.LOBBY:
                response = {'status': Status.LOBBY, 'playerlist': list(PLAYERS.keys())}




            # Send response message back to client
            sendJSON(playerSocket, response)
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
            playerObj = Player(name)
            # json_status = {'status': Status.VALID, 'player': playerObj.__dict__()}
            json_status = {'status': Status.VALID, 'name': name}
            # Add player to active players
            PLAYERS[name] = [sock, addr, playerObj]
            print(f"  -> {name} logged into server from {addr[0]}:{addr[1]}")
            print(f"{len(PLAYERS)} total players {list(PLAYERS.keys())}")

    return json_status
      
def updateLobby():
    global PLAYERS
    names = list(PLAYERS.keys())
    for sock,_,_ in PLAYERS.values():
        pass
    return

# Starts the game
def start_game():
    print("Starting game")
    pass


# Quits the server
def quit_server():
    global PLAYERS
    global GAME
    global SHUTDOWN
    json = {'status': Status.SHUTDOWN}
    for _, (sock, _, _) in PLAYERS.items():
        sendJSON(sock, json)
    SHUTDOWN = True
    sys.exit()


def recvJSON(sock: socket) -> dict:
    data = json.loads(sock.recv(1024).decode('utf-8'))
    return data

def sendJSON(sock: socket, data) -> None:
    # print(type(data), data)
    json_data = json.dumps(data, indent=4)
    # print(json_data)
    sock.send(json_data.encode('utf-8'))



if __name__ == "__main__":
    start_server()
    quit_server()