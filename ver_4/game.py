import sys, random as rand, math

sys.path.append('ver_4/objects')
sys.path.append('ver_4/logs')
from ships import *
from player import *
from logger import *
from colony import *
from ship_data import *


class Game:
  def __init__(self, players, random_seed=None, board_len = 7, log_name='log'):
    self.players = players
    self.set_player_nums()
    self.log = Logger(f'ver_4/logs/{log_name}.txt')
    self.log.clear_log()

    rand.seed(random_seed)

    self.board = {}
    
    self.board_len = board_len
    self.turn = 0
    self.winner = None
    self.combat_coords = []

    self.initialize_board()

    
  def set_player_nums(self):
    for i, player in enumerate(self.players):
      player.player_num = i+1

  def initialize_board(self):
    self.log.initialize(self.players)
    for i, player in enumerate(self.players):
      starting_coord = (self.board_len//2, (player.player_num-1)*(self.board_len-1))

      hc = Colony(player.player_num, starting_coord, is_hc=True)
      player.home_colony = hc
      self.add_to_board(hc)

      bought_ships = player.strategy.buy_ships(player.cp)
      cp_used = self.get_cp_of_dict(bought_ships)
      if cp_used > player.cp:
        self.log.write(f'Player {player.player_num} used too much CP, no ships bought!\n')
        continue
      
      player.cp -= cp_used
      for key in bought_ships:
        for num_ships in range(bought_ships[key]):
          ship = ship_objects[key](i+1, hc.coords, num_ships+1)
          self.add_to_board(ship)
          player.ships.append(ship)
          player.ship_counter[ship.name] += 1
    self.turn = 1
  

  def movement_phase(self):
    self.log.begin_phase(self.turn, 'MOVEMENT')
    for player in self.players:
      for ship in player.ships:
        self.update_combat_coords()
        if ship.coords not in self.combat_coords:
          translations = self.get_in_bounds_translations(ship.coords)
          chosen_move = player.strategy.choose_translation(ship.__dict__, translations)
          orig = ship.coords
          self.move_ship(ship, chosen_move)
          self.log.log_move_ship(ship, orig, ship.coords)
          self.update_combat_coords()
      self.log.write('\n')
    
    self.log.end_phase(self.turn, 'MOVEMENT')
    self.log.write(f'\nCombat Coords: {self.combat_coords}\n')
  
  def combat_phase(self):
    self.log.begin_phase(self.turn, 'COMBAT')
    used_coords = []
    combat = True if len(self.combat_coords) != 0 else False
    for coord in self.combat_coords:
      self.log.log_combat_location(coord)
      sort_cls = sorted(self.all_ships(coord), key=lambda x: x.ship_class)
      for ship in sort_cls:
        if ship.hp == 0:
          continue
        if not self.check_for_opponent_ships(ship.player_num, ship.coords):
          continue

        player = self.players[ship.player_num - 1]
        enemies = self.get_enemies(ship, sort_cls)
        combat_order = [obj.__dict__ for obj in sort_cls]
        target_dict = player.strategy.choose_target(ship.__dict__, combat_order)
        target = self.dict_to_obj(target_dict, enemies)

        self.log.combat_ships(ship, target)
        if self.hit(ship, target):
          self.log.write('\n\t\tHit!\n')
          dmg = 1
          target.hp -= dmg
          self.log.ship_hit(ship, target, dmg)
          if target.hp == 0:
            self.log.ship_destroyed(target)
            self.dead_ship(target)
        else:
          self.log.write('\n\t\tMiss\n')
        
      for ship in sort_cls:
        if ship.hp == 0:
          sort_cls.remove(ship)
      used_coords.append(coord)
    for coord in used_coords:
      self.combat_coords.remove(coord)

    if combat:
      self.log.write('\n\t\tRemaining Ships:\n')
      for player in self.players:
        for ship in player.ships:
          self.log.write(f'\t\tPlayer {player.player_num} {ship.name} {ship.ship_num}\n')
    self.log.end_phase(self.turn, 'COMBAT')
  
  def economic_phase(self):
    self.log.begin_phase(self.turn, 'ECONOMIC')
    for player in self.players:
      self.log.write(f'\tPlayer {player.player_num}:\n')
      player.cp += 10
      self.log.write(f'\t\tAvailable CP: {player.cp}')
      sorted_ships = sorted(player.ships, reverse=True, key=lambda x: x.maint_cost)
      used_cp = 0
      for ship in sorted_ships:
        if player.cp < ship.maint_cost:
          self.log.write(f'\n\t\tNot Enough CP! Removing {ship.name} {ship.ship_num}')
          self.dead_ship(ship)
        else:
          player.cp -= ship.maint_cost
          used_cp += ship.maint_cost
      self.log.write(f'\n\t\tUsed CP: {used_cp}\n\t\tRemaining CP: {player.cp}\n')

      bought_ships = player.strategy.buy_ships(player.cp)
      cp_used = self.get_cp_of_dict(bought_ships)
      if cp_used > player.cp:
        self.log.write(f'Player {player.player_num} used too much CP, no ships bought!\n')
        continue
      
      player.cp -= cp_used
      if bought_ships != None:
        for key in bought_ships:
          for num_ships in range(bought_ships[key]):
            ship = ship_objects[key](player.player_num, player.home_colony.coords, player.ship_counter[key]+1)
            self.add_to_board(ship)
            player.ships.append(ship)
            player.ship_counter[ship.name] += 1

    self.log.end_phase(self.turn, 'ECONOMIC')
  
  def run_to_completion(self, max_turns = 999999999, debug=False):
    self.check_winner()
    
    while self.winner is None and self.turn <= max_turns:
      if debug:
        self.print_board()
      self.movement_phase()
      self.combat_phase()
      self.economic_phase()
      self.check_winner()
      self.turn += 1
      if debug:
        self.print_board()
    self.log.player_win(self.winner)
  
  #HELPER FUNCTIONS
  def get_in_bounds_translations(self, coords):
    if coords == None: return []
    in_bounds_translations = []
    
    for translation in [(0,0), (0,1), (0,-1), (1,0), (-1,0)]:
      new_x, new_y = (coords[0]+translation[0], coords[1]+translation[1])
      if 0 <= new_x <= self.board_len-1 and 0 <= new_y <= self.board_len-1:
        in_bounds_translations.append(translation)
    return in_bounds_translations

  def check_winner(self):
    for player in self.players:
      winner = self.check_for_opponent_ships(player.player_num,player.home_colony.coords, return_pn=True)
      if type(winner) == int:
        self.winner = winner

  def add_to_board(self, obj):
    if obj.coords not in self.board:
      self.board[obj.coords] = [obj]
    else:
      self.board[obj.coords].append(obj)
    self.update_simple_board()
        
  def remove_from_board(self, obj):
    self.board[obj.coords].remove(obj)
    if len(self.board[obj.coords]) == 0:
      del self.board[obj.coords]
    self.update_simple_board()

  def move_ship(self, ship, translation):
    if translation not in self.get_in_bounds_translations(ship.coords):
      self.log.write('\tInvalid Move, Skipping...\n')
    else:
      self.remove_from_board(ship)
      ship.coords = (ship.coords[0]+translation[0], ship.coords[1]+translation[1])
      self.add_to_board(ship)      

  def check_for_opponent_ships(self, player_num, coords, return_pn=False):
    x, y = coords
    for obj in self.board[coords]:
      if obj.player_num != player_num and obj.obj_type == 'Ship':
        if return_pn:
          return obj.player_num
        return True
    return False

  def check_for_ally_ships(self, ship_list):
    return len(set([ship.player_num for ship in ship_list])) == 1

  def all_ships(self, coord):
    return [obj for obj in self.board[coord] if obj.obj_type == 'Ship']

  def get_enemies(self, ship, combat_list):
    return [obj for obj in combat_list if obj.player_num != ship.player_num]

  def roll(self):
    return random.randint(1,10)
    
  def hit(self, attacker, defender):
    roll = self.roll()
    atk_value = attacker.atk - defender.df
    if roll <= atk_value or roll == 1:
      return True
    return False
  
  def dead_ship(self, ship):
    player = self.players[ship.player_num - 1]
    player.ships.remove(ship)
    self.remove_from_board(ship)

  def dict_to_obj(self, obj_dict, obj_list): #obj list = list that the desired object is in
    for obj in obj_list:
      if obj.name == obj_dict['name']:
        if obj.ship_num == obj_dict['ship_num']:
          if obj.player_num == obj_dict['player_num']:
            return obj

  def get_cp_of_dict(self, ships_dict):
    if ships_dict == None:
      return 0
    total_cp = 0
    for key in ships_dict:
      for ship in all_ships:
        if ship['name'] == key:
          total_cp += ships_dict[key]*ship['cp_cost']
    return total_cp

  def update_combat_coords(self):
    for player in self.players:
      for ship in player.ships:
        if self.check_for_opponent_ships(ship.player_num,ship.coords):
          if ship.coords not in self.combat_coords:
            self.combat_coords.append(ship.coords)

  def update_simple_board(self):
    strat_board = {}
    for key in self.board:
      strat_board[key] = [obj.__dict__ for obj in self.board[key]]
    for player in self.players:
      player.strategy.simple_board = strat_board
      player.strategy.turn = self.turn


  def print_board(self):
    temp_dict = {}
    for key in self.board:
      temp_dict[key] = []
      for obj in self.board[key]:
        if isinstance(obj, Colony):
          temp_dict[key].append(('Colony', obj.player_num))
        else:
          temp_dict[key].append((obj.name, obj.player_num))
    return temp_dict