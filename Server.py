import sys
import os
import time
import json
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, timeout, gethostname, gethostbyname
import urllib.request
import json
import threading
# import pygame

from src.game import Game
from src.player import Player


PLAYERS = {}                        # holds active players in format { <username>: [<socket>, <address>], ...}
T_LOCK = threading.Condition()      # thread lock
# pygame.init()

def getIP():
    return json.loads(urllib.request.urlopen('https://jsonip.com/').read())['ip']

def start_server():
    global PLAYERS
    global T_LOCK

    if len(sys.argv) == 1:
        ADDR = 'localhost'
        PORT = 9229
    elif len(sys.argv) == 2:
        # ADDR = sys.argv[1]
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
            time.sleep(0.5)

    SOCKET.close()


# ! THREADED FUNCTION
def playerThread(playerSocket, playerAddress):
    global PLAYERS
    global T_LOCK

    playerName = newPlayerThread(playerSocket, playerAddress)
    
    # Handle player commands
    while True:
        # Handle incoming client request
        with T_LOCK:
            try:
                # Receive command from client
                data = recvJSON(playerSocket)
            except:
                T_LOCK.notify()
                continue

            # print(f"{user} issued {code} command")
            print(f"RECEIVED: {data}")
            # print(f"{data.get('status')}")
            if data.get('disconnect') == 1:
                PLAYERS.pop(data['name'])
                print(f"{len(PLAYERS)} total players {list(PLAYERS.keys())}")


            # Send response message back to client
            # sendJSON(playerSocket, response)

            T_LOCK.notify()
                    
    return



# ! THREADED FUNCTION
def newPlayerThread(playerSocket, playerAddress):
    global PLAYERS
    global T_LOCK

    playerName = None
    # Loop while client is not logged into server
    while True:
        with T_LOCK:  
            # Receive player's name
            try:
                data = recvJSON(playerSocket)
            except:
                T_LOCK.notify()
                continue

            playerName = data['name']
            # print(f"Received: {playerName}")
            # Player entered a name already active
            if PLAYERS.get(playerName) != None:
                print(f"Player '{playerName}' already exists")
                # Send BAD message
                json_status = {'status': 0}
                sendJSON(playerSocket, json_status)

            # Player enters a new name
            else:
                # Send OK message
                json_status = {'status': 1}
                sendJSON(playerSocket, json_status)
                break
            T_LOCK.notify()

    # Add player to active players
    PLAYERS[playerName] = [playerSocket, playerAddress, Player(playerName)]
    print(f"\t-> {playerName} logged into server from {playerAddress[0]}:{playerAddress[1]}")

    print(f"{len(PLAYERS)} total players {list(PLAYERS.keys())}")

    return playerName

    

def recvJSON(sock: socket) -> dict:
    data = json.loads(sock.recv(1024).decode('utf-8'))
    return data

def sendJSON(sock: socket, data) -> None:
    sock.send(json.dumps(data).encode('utf-8'))





if __name__ == "__main__":
    start_server()
    sys.exit()