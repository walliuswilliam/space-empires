import math
from random import random

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
    ship.set_player_number(self.player_number)
    self.ships.append(ship)

  def choose_translation(self, board, translations, ship, opponent_hc):
    my_ship_coords = ship.coords
    opp_hc_coords = opponent_hc.coords

    best_move = translations[0]

    for translation in translations:
      choice_coords = (my_ship_coords[0]+translation[0], my_ship_coords[1]+translation[1])
      best_coords = (my_ship_coords[0]+best_move[0], my_ship_coords[1]+best_move[1])
      choice_distance = self.calc_distance(choice_coords, opp_hc_coords)
      best_distance = self.calc_distance(best_coords, opp_hc_coords)

      if choice_distance < best_distance:
        best_move = translation
    return best_move
  
  def calc_distance(self, point1, point2):
    return abs(math.sqrt((point2[0]-point1[0])**2+(point2[1]-point1[1])**2))



class RandomPlayer():
  def __init__(self):
    self.player_num = None
    self.home_colony = None

  def set_player_num(self, n):
    self.player_num = n

  def choose_translation(self, game_state, choices):
    random_idx = math.floor(len(choices) * random())
    return choices[random_idx]