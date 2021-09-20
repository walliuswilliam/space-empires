import math
import random
from strategy import *


class CustomPlayer():
  def __init__(self):
    self.player_num = None
    self.ships = []
    self.home_colony = None

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
    strat = Strategy()
    return strat.move(board, translations, ship, opponent_hc)

  def choose_target(self, targets):
    strat = Strategy()
    return strat.attack(targets)
    

class RandomPlayer():
  def __init__(self):
    self.player_num = None
    self.home_colony = None

  def set_player_num(self, n):
    self.player_num = n

  def choose_translation(self, game_state, choices):
    random_idx = math.floor(len(choices) * random())
    return choices[random_idx]


class TestPlayer():
  def __init__(self):
    self.player_num = None
    self.ships = []
    self.home_colony = None

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
    strat = Dumb()
    return strat.move(board, translations, ship, opponent_hc)

  def choose_target(self, targets):
    strat = Dumb()
    return strat.attack(targets)