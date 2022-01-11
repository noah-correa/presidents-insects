'''
File:           status.py
Author:         Noah Correa
Date:           09/9/21
Description:    Contains the Status class which defines the codes sent between the Client and Server
'''

class Status():
    # Server codes
    CONNECT     =   100     # Connect client to server
    DISCONNECT  =   101     # Disconnect client from server
    SHUTDOWN    =   102     # Server shutdown 
    
    # Validation codes
    VALID       =   200     # Valid move requested by client
    INVALID     =   201     # Invalid move requested by client
    
    # Server requests
    PLAYER      =   300     # Server requests client to set the player object
    GAME        =   301     # Server/Client game 

    # Client requests
    LOBBY       =   400     # Client requesting lobby information
    MOVE        =   401     # Client requesting a move