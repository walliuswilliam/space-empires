import sys
from players import *
from game import *


# players = [CustomPlayer(), CustomPlayer()]
# game = Game(players, random_seed=1)
# game.run_to_completion()


players = [TestPlayer(), TestPlayer()]
game = Game(players, random_seed=1)
game.run_to_completion()