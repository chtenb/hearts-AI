from game import Game
from player import StupidPlayer, SimplePlayer


# These four players are playing the game
players = [SimplePlayer(), SimplePlayer(), SimplePlayer(), SimplePlayer()]

# We are simulating n games accumulating a total score
scores = (0, 0, 0, 0)
for game_nr in range(1000):
    print('Game {}'.format(game_nr))
    game = Game(players)
    scores = tuple(sum(x) for x in zip(scores, game.play()))

print(scores)
