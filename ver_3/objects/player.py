import math, random

class Player:
  def __init__(self, strat):
    self.player_num = None
    self.ships = []
    self.home_colony = None
    self.strategy = strat
    self.cp = 200
