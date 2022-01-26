import random, math, sys
sys.path.append('')
from ship_data import *
import math

class MoveToOpponent:
    def __init__(self):
        self.simple_board = None
        self.turn = 0

    def min_distance_translation(self, ship_info, choices, target_coords):

        if choices != []:
            
            min_choice = None
            min_distance = 999

            for choice in choices:

                new_point = [a + b for a, b in zip(ship_info['coords'], choice)]
                distance = math.dist(new_point, target_coords)

                if distance < min_distance:
                    min_distance = distance
                    min_choice = choice

            return min_choice

    def get_opponent_home_colony_coords(self, ship_info):
        for key, value in self.simple_board.items():
            for info in value:
                if info['obj_type'] == 'Colony' and info['is_home_colony'] and info['player_num'] != ship_info['player_num']:
                    return key

    def choose_translation(self, ship_info, choices):
        target_coords = self.get_opponent_home_colony_coords(ship_info)
        return self.min_distance_translation(ship_info, choices, target_coords)
  
    def choose_target(self, ship_info, simplified_combat_order):
        for info in simplified_combat_order:
            if info['player_num'] != ship_info['player_num']:
                return info

    def buy_ships(self, cp_budget):

        if self.turn == 0:
            return {'Dreadnaught': 4}
        elif (self.turn % 2) == 0:
            return {'Dreadnaught': 1}

        return {}
