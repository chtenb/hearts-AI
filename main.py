# We assume
from game import Game
from player import StupidPlayer, SimplePlayer

# SimplePlayer()

scores = (0, 0, 0, 0)

for _ in range(100):
    game = Game([SimplePlayer(), StupidPlayer(), StupidPlayer(), StupidPlayer()])
    scores = tuple(sum(x) for x in zip(scores, game.play()))

print(scores)
