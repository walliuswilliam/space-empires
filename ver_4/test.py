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
from cayden import CaydenStrat
from charlie import MoveToOpponent as CharlieStrat
from justin import CompetitionStrat as JustinStrat
from maia import BattleStrat as MaiaStrat

##Normal game

# print('running normal game...')
# players = [Player(MoveToColony()), Player(MoveToColony())]
# game = Game(players, random_seed=1)
# game.run_to_completion()
# print(game.winner)
# print('passed\n')


winners = {1:0, 2:0}
for i in range(50):
    players = [Player(AntonStrat()), Player(MaiaStrat())]
    game = Game(players)

    game.run_to_completion(max_turns=100)
    try:
        winners[game.winner] += 1
    except:
        None

for i in range(50):
    players = [Player(MaiaStrat()), Player(AntonStrat())]
    game = Game(players)

    game.run_to_completion(max_turns=100)
    try:
        winners[3-game.winner] += 1
    except:
        None
print(winners)
