from socket import socket, AF_INET, SOCK_STREAM
import sys
import time
import json

from src.player import Player
from src.card import Card

PLAYER = None

def start_client():

    if len(sys.argv) == 1:
        ADDR = 'localhost'
        PORT = 9229 
    elif len(sys.argv) == 2:
        ADDR, PORT = sys.argv[1].split(':')
        PORT = int(PORT)
        # ADDR = sys.argv[1]
        # PORT = int(sys.argv[2])
    else:
        print("Usage: python TestClient.py <server address> <server port>")
        sys.exit()


    # Create socket
    SOCKET = socket(AF_INET, SOCK_STREAM)

    # Connect to server
    SOCKET.connect((ADDR, PORT))
    print(f"Connected to server {ADDR}:{PORT}")

    name = input("Enter your name: ")
    while True:
        json_name = {'name': name}
        sendJSON(SOCKET, json_name)
        data = recvJSON(SOCKET)
        status = data['status']
        
        if status == 1:
            # Valid name
            break
        print(f"User with name '{name}' already exists")
        name = input("Enter a different name: ")

    PLAYER = Player(name)

    i = 0
    while i < 30:
        i += 1
        time.sleep(1)

    # disconnect(SOCKET)
    SOCKET.close()

    return

def recvJSON(sock: socket) -> dict:
    data = json.loads(sock.recv(1024).decode('utf-8'))
    return data

def sendJSON(sock: socket, data) -> None:
    sock.send(json.dumps(data).encode('utf-8'))

def disconnect(sock: socket):
    json_disconnect = {'player': PLAYER, 'status': 0}
    sendJSON(sock, json_disconnect)

if __name__ == "__main__":
    start_client()