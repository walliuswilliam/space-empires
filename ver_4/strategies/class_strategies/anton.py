from random import random
from ship_data import *
import math


class CustomStrategy():
  def __init__(self):
    self.simple_board = {}
    self.turn = 0
  
  def update_simple_board(self, updated_board):
    self.simple_board = updated_board

  def get_opponent_ships(self, ship_info, combat_order_info):
    return [obj_info for obj_info in combat_order_info if obj_info['player_num'] != ship_info['player_num'] and obj_info['hp'] > 0]

  def calc_distance(self, point_1, point_2):
    return (abs(point_2[0]-point_1[0])**2 + abs(point_2[1]-point_1[1])**2)**0.5

  def find_home_colonies(self, ship_info):
    coords = []
    for coord in self.simple_board:
      for obj_info in self.simple_board[coord]:
        is_opponent_home_colony = obj_info['obj_type'] == 'Colony' and obj_info['is_home_colony'] and obj_info['player_num'] != ship_info['player_num']
        if is_opponent_home_colony:
          coords.append(coord)

    return coords

  def find_min_choice(self, choices, coord):
    min_choice = choices[0]
    min_distance = self.calc_distance(min_choice, coord)

    for choice in choices:
      if self.calc_distance(choice, coord) < min_distance:
        min_choice = choice
        min_distance = self.calc_distance(choice,coord)
    return min_choice

  def min_distance_translation(self, choices, ship_info, target_coords):
    if choices != []:
      min_choice = choices[0]
      min_distance = self.calc_distance((ship_info['coords'][0] + min_choice[0], ship_info['coords'][1] + min_choice[1]), target_coords)
      for choice in choices:
        current_coords = (ship_info['coords'][0] + choice[0], ship_info['coords'][1] + choice[1])
        current_distance = self.calc_distance(current_coords, target_coords)

        if current_distance < min_distance:
          min_distance = current_distance
          min_choice = choice
      
      return min_choice

  def choose_translation(self, ship_info, choices):
    ship_coords = ship_info['coords']
    player_num = ship_info['player_num']
    target_coords = self.find_min_choice(self.find_home_colonies(ship_info), ship_coords)
    return self.min_distance_translation(choices, ship_info, target_coords)
    
  def choose_target(self, ship_info, combat_order_info):
    opponent_ship_infos = self.get_opponent_ships(ship_info,combat_order_info)
    random_idx = math.floor(len(opponent_ship_infos) * random())
    return opponent_ship_infos[random_idx]

  def buy_ships(self, cp_budget):
    if self.turn == 0:
      return {'Dreadnaught':5}
    elif self.turn%2 == 0:
      return {'Dreadnaught':2*cp_budget//(3*dreadnaught['cp_cost'])}
