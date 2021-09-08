

from src.game import Game
from src.player import Player
from src.move import Move



G = Game()

a = G.addNewPlayer("A")
b = G.addNewPlayer("B")
c = G.addNewPlayer("C")
d = G.addNewPlayer("D")
e = G.addNewPlayer("E")
f = G.addNewPlayer("F")
f2 = G.addNewPlayer("F")

print(f"a = {a}")
print(f"b = {b}")
print(f"c = {c}")
print(f"d = {d}")
print(f"e = {e}")
print(f"f = {f}")
print(f"f2 = {f2}")

print(str(G))
G.startMP()
print(str(G))
