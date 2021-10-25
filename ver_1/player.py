import math
import random
from strategy import *


class Player():
  def __init__(self, strat):
    self.player_num = None
    self.ships = []
    self.home_colony = None
    self.strategy = strat

  def set_player_num(self, n):
    self.player_num = n

  def get_opponent_player_num(self):
    if self.player_num == None:
      return None
    elif self.player_num == 1:
      return 2
    elif self.player_num == 2:
      return 1

  def add_ship(self, ship):
    ship.set_player_num(self.player_num)
    self.ships.append(ship)

  def choose_translation(self, board, translations, ship, opponent_hc):
    return self.strategy.move(board, translations, ship, opponent_hc)

  def choose_target(self, targets):
    return self.strategy.attack(targets)
    