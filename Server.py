import sys
import os
import time
import json
import argparse
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, timeout, gethostname, gethostbyname
import urllib.request
import json
import threading

from src.game import Game
from src.player import Player


PLAYERS = {}                        # holds active players in format { <username>: [<socket>, <address>], ...}
T_LOCK = threading.Condition()      # thread lock


def start_server():
    global PLAYERS
    global T_LOCK

    if len(sys.argv) == 1:
        ADDR = 'localhost'
        PORT = 9229
    elif len(sys.argv) == 2:
        # ADDR = sys.argv[1]
        PORT = int(sys.argv[1])
    else:
        print("Usage: python Server.py <server address> <server port>")
        sys.exit()

    s = gethostbyname(gethostname())
    print(s)

    ADDR = s
    print(f"Starting server at {ADDR}:{PORT}")

    SOCKET = socket(AF_INET, SOCK_STREAM)
    SOCKET.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    SOCKET.bind((ADDR, PORT))
    SOCKET.listen(1)
    SOCKET.setblocking(False)

    GAME = Game()

    while True:
        try:
            # Accept a client and create a thread for it
            playerSocket, playerAddress = SOCKET.accept()
            print(f"{playerAddress} connected")
            threading.Thread(target=newPlayerThread, args= (playerSocket, playerAddress)).start()
        except BlockingIOError as e:
            continue
        except OSError as e:
            break
        finally:
            time.sleep(0.1)

    SOCKET.close()



def newPlayerThread(playerSocket, playerAddress):
    global PLAYERS
    global T_LOCK

    # Loop while client is not logged into server
    print("Client connected")
    while True:
        with T_LOCK:  
            # Receive client's username
            data = json.loads(playerSocket.recv(1024).decode('utf-8'))
            playerName = data['name']
            print(f"Received: {playerName}")
            # Client entered a username already logged into server
            if PLAYERS.get(playerName) != None:
                playerSocket
                pass

            # Client enters a new username
            else:
                print("New User")
                # playerSocket.send((NEW_USER + "\r\nNew user\r\n\r\n").encode('utf-8'))
                
                # playerSocket.send((OK + "\r\nUser added\r\n\r\n").encode('utf-8'))
                break
            T_LOCK.notify()

    # Add player to active players
    PLAYERS[playerName] = [playerSocket, playerAddress, Player(playerName)]
    print(f"\t-> {playerName} logged into server from {playerAddress[0]}:{playerAddress[1]}")

    print(f"{len(PLAYERS)} total players {list(PLAYERS.keys())}")

    return playerName

    

def recvJSON(socket):
    data = json.loads(socket.recv(1024).decode('utf-8'))
    return data

def sendJSON(socket, data):
    json_data = json.loads()





if __name__ == "__main__":
    start_server()
    sys.exit()