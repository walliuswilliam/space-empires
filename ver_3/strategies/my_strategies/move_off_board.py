import math,random

class MoveOffBoard:
  def choose_translation(self, ship_info, possible_translations):
    return (0,1)

  def choose_target(self, targets):
    return targets[random.randint(0,len(targets)-1)]
    