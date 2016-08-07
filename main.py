from game import Game
from player import StupidPlayer, SimplePlayer

# SimplePlayer()

# players = [StupidPlayer(), StupidPlayer(), StupidPlayer(), StupidPlayer()]
# players = [SimplePlayer(), SimplePlayer(), StupidPlayer(), StupidPlayer()]
players = [SimplePlayer(), SimplePlayer(), SimplePlayer(), SimplePlayer()]
scores = (0, 0, 0, 0)

for _ in range(1000):
    print(_)
    game = Game(players)
    scores = tuple(sum(x) for x in zip(scores, game.play()))

print(scores)
