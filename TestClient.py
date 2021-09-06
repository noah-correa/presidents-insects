from socket import socket, AF_INET, SOCK_STREAM
import sys
import time
import json

from src.player import Player

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

    name = input("Enter your name: ")

    # Create socket
    SOCKET = socket(AF_INET, SOCK_STREAM)

    # Connect to server
    SOCKET.connect((ADDR, PORT))
    print(f"Connected to server {ADDR}:{PORT}")

    json_name = {'name': name}
    

    SOCKET.send(json.dumps(json_name).encode('utf-8'))

    i = 0
    while i < 30:
        i += 1
        time.sleep(1)

    SOCKET.close()

    return



if __name__ == "__main__":
    start_client()