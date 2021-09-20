import math
import random

class Strategy:

  def move(self, board, translations, ship, opponent_hc):
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
  
  def attack(self, targets):
    return targets[random.randint(0,len(targets)-1)]


class Dumb:
  def move(self, board, translations, ship, opponent_hc):
    return (0,1)

  def attack(self, targets):
    return targets[random.randint(0,len(targets)-1)]

  