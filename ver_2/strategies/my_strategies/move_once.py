import math,random

class MoveOnce:
  def choose_translation(self, ship_info, possible_translations):
    ship_coords = ship_info['coords']
    
    for coord in self.simple_board:
      for obj in self.simple_board[coord]:
        if obj['obj_type'] == 'Colony':
          if obj['is_home_colony'] == True and obj['player_num'] == ship_info['player_num']:
            hc_coords = obj['coords']
    
    if ship_coords == hc_coords:
      return (-1,0)
    return (0,0)

  def choose_target(self, targets):
    return targets[random.randint(0,len(targets)-1)]
    