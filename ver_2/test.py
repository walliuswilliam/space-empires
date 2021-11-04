import sys
sys.path.append('ver_2/objects')
from player import *
from game import *


sys.path.append('ver_2/strategies/my_strategies')
from move_off_board import *
from move_once import *
from move_to_colony import *

sys.path.append('ver_2/strategies/class_strategies')
from anton import CustomStrategy as AntonStrat
from cayden import MoveToEnemyHomeColony as CaydenStrat
from charlie import MoveToOpponent as CharlieStrat
from justin import MoveToClosestCol as JustinStrat
from maia import StraightToEnemyColony as MaiaStrat

##Normal game

print('running normal game...')
players = [Player(MoveToColony()), Player(MoveToColony())]
game = Game(players, random_seed=1)
game.run_to_completion()
assert game.winner == 1
print('passed\n')


##Testing if player can move ship off board
print('testing ship moving off board...')
players = [Player(MoveToColony()), Player(MoveOffBoard())]
game = Game(players, random_seed=1)
game.run_to_completion(max_turns=3)

init_coords = players[1].ships[0].coords
game.movement_phase()
post_coords = players[1].ships[0].coords

assert init_coords == post_coords
print('passed\n')


##Defender fires first
print('checking that defender fires first...')
players = [Player(MoveToColony()), Player(MoveOnce())]
game = Game(players, random_seed=1)

game.run_to_completion(max_turns=4)
game.movement_phase()
assert game.all_ships(game.combat_coords[0])[0].player_num == 2
print('passed\n')
 

##Game ends when ship is on opp hc
print('checking game correctly identifies winner...')
players = [Player(MoveToColony()), Player(MoveToColony())]
game = Game(players, random_seed=1)

game.run_to_completion()
assert game.winner == 1
print('passed\n')



print("checking anton's strategy")
players = [Player(AntonStrat()), Player(MoveToColony())]
game = Game(players, random_seed=1)

game.run_to_completion()
print('passed\n')


print("checking charlie's strategy")
players = [Player(CharlieStrat()), Player(MoveToColony())]
game = Game(players, random_seed=1)

game.run_to_completion()
print('passed\n')


print("checking maia's strategy")
players = [Player(MaiaStrat()), Player(MoveToColony())]
game = Game(players, random_seed=1)

game.run_to_completion()
print('passed\n')


# print("checking cayden's strategy")
# players = [Player(CaydenStrat()), Player(MoveToColony())]
# game = Game(players, random_seed=1)

# game.run_to_completion()
# print('passed\n')


# print("checking justin's strategy")
# players = [Player(JustinStrat()), Player(MoveToColony())]
# game = Game(players, random_seed=1)

# game.run_to_completion()
# print('passed\n')