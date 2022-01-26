import sys
sys.path.append('ver_4')
import math,random
from ship_data import *

class Custom:
  def __init__(self):
    self.simple_board = None
    self.turn = 0
    self.player_num = None
  
  def choose_translation(self, ship_info, possible_translations):
    if self.player_num == None:
      self.player_num = ship_info['player_num']
    
    my_ship_coords = ship_info['coords']
    my_ship_num = ship_info['ship_num']
    op_player_num = 1 if self.player_num == 2 else 2

    for coord in self.simple_board:
      for obj in self.simple_board[coord]:
        if obj['obj_type'] == 'Colony':
          if obj['is_home_colony'] == True and obj['player_num'] == ship_info['player_num']:
            my_hc_coords = obj['coords']
          if obj['is_home_colony'] == True and obj['player_num'] == op_player_num:
            opp_hc_coords = obj['coords']

    best_translation = possible_translations[0]

    for translation in possible_translations:
      choice_coords = (my_ship_coords[0]+translation[0], my_ship_coords[1]+translation[1])
      best_coords = (my_ship_coords[0]+best_translation[0], my_ship_coords[1]+best_translation[1])
      choice_distance = math.dist(choice_coords, opp_hc_coords)
      best_distance = math.dist(best_coords, opp_hc_coords)

      if choice_distance < best_distance:
        best_translation = translation
    
    return best_translation
      
  def choose_target(self, ship_info, combat_order):
    possible_targets = self.filter_own_ships(ship_info['player_num'], combat_order)
    return possible_targets[random.randint(0,len(possible_targets)-1)]   
  
  def filter_own_ships(self, own_player_num, combat_order, ship_type=None):
    if ship_type is None:
      return [ship_dict for ship_dict in combat_order if ship_dict['player_num'] != own_player_num]
    else:
      return [ship_dict for ship_dict in combat_order if ship_dict['player_num'] != own_player_num and ship_dict['name'] == ship_type]

  def buy_ships(self, cp_budget):
    bought_ships = {'Dreadnaught': 0}

    if cp_budget < 12:
      return None

    #Initial Purchase
    if self.turn == 0:
      bought_ships = {'Cruiser': 1, 'Dreadnaught': 4}

    elif self.turn == 1:
      bought_ships = {'BattleCruiser': 1, 'Cruiser': 1, 'Dreadnaught': 1}

    #Mid game purchases
    else:
      while self.get_cp_of_dict(bought_ships) < cp_budget:
        bought_ships['Dreadnaught'] += 1
      if self.get_cp_of_dict(bought_ships) > cp_budget:
        bought_ships['Dreadnaught'] -= 1
    
    return bought_ships
    
  def get_cp_of_dict(self, ships_dict):
    total_cp = 0
    for key in ships_dict:
      for ship in all_ships:
        if ship['name'] == key:
          total_cp += ships_dict[key]*ship['cp_cost']
    return total_cp
