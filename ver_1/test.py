import sys
from player import *
from game import *
from strategy import *

##Normal game

print('running normal game...')
players = [Player(Custom()), Player(Custom())]
game = Game(players, random_seed=1)
game.run_to_completion()
assert game.winner == 1
print('passed\n')


##Testing if player can move ship off board
print('testing ship moving off board...')
players = [Player(Custom()), Player(MoveOffBoard())]
game = Game(players, random_seed=1)
game.run_to_completion(max_turns=3)

init_coords = players[1].ships[0].coords
game.movement_phase()
post_coords = players[1].ships[0].coords

assert init_coords == post_coords
print('passed\n')


##Defender fires first
print('checking that defender fires first...')
players = [Player(Custom()), Player(MoveOnce())]
game = Game(players, random_seed=1)

game.run_to_completion(max_turns=4)
game.movement_phase()
assert game.all_ships(game.combat_coords[0])[0].player_num == 2
print('passed\n')
 

##Game ends when ship is on opp hc
print('checking game correctly identifies winner...')
players = [Player(Custom()), Player(Custom())]
game = Game(players, random_seed=1)

game.run_to_completion()
assert game.winner == 1
print('passed\n')
