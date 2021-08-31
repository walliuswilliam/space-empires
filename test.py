import sys
from players import *
from game import *


players = [CustomPlayer(), CustomPlayer()]
game = Game(players, random_seed=1)
game.complete_movement_phase()

