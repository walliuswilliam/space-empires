import sys
sys.path.append('ver_4/objects')
from player import *
from game import *


sys.path.append('ver_4/strategies/my_strategies')
from move_off_board import *
from move_once import *
from move_to_colony import *
from custom import *
from wall_strat import WallStrat as WilliamStrat

sys.path.append('ver_4/strategies/class_strategies')
from anton import SmartRush as AntonStrat
from cayden import CaydenCompStrat as CaydenStrat
from charlie import MoveToOpponent as CharlieStrat
from justin import CompetitionStrat as JustinStrat
from maia import BattleStrat as MaiaStrat

##Normal game

# print('running normal game...')
# players = [Player(Custom()), Player(Custom())]
# game = Game(players, random_seed=1)
# game.run_to_completion(max_turns=100)
# print(f'player {game.winner} wins')
# print('passed\n')



##Comp

winners = {1:0, 2:0, 'Ties':0}
for i in range(50):
    players = [Player(CaydenStrat()), Player(Custom())]
    game = Game(players)

    game.run_to_completion(max_turns=100)
    try:
        winners[game.winner] += 1
    except:
        winners['Ties'] += 1

for i in range(50):
    players = [Player(Custom()), Player(CaydenStrat())]
    game = Game(players)

    game.run_to_completion(max_turns=100)
    try:
        winners[3-game.winner] += 1
    except:
        winners['Ties'] += 1
print(winners)
