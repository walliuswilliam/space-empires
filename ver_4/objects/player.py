import math, random, sys
sys.path.append('ver_3')
from ship_data import *

class Player:
  def __init__(self, strat):
    self.player_num = None
    self.ships = []
    self.home_colony = None
    self.strategy = strat
    self.cp = 200
    self.ship_counter = {ship_name:0 for ship_name in ship_objects.keys()}
