import sys, random as rand, math

sys.path.append('ver_2/logs')
from ships import *
from player import *
from logger import *
from colony import *


class Game:
  def __init__(self, players, random_seed=None, board_size=[7,7], log_name=None):
    self.players = players
    self.set_player_nums()
    if log_name is None:
      self.log = Logger('ver_2/logs/log.txt')
    else:
      self.log = Logger('ver_2/logs/{}.txt'.format(log_name))
    self.log.clear_log()

    rand.seed(random_seed)

    global board_x,board_y, mid_x, mid_y

    board_x, board_y = board_size
    mid_x = (board_x + 1) // 2
    mid_y = (board_y + 1) // 2

    self.board = [[[] for _ in range(board_x)] for _ in range(board_y)]
    self.initialize_board()
    
    self.board_size = board_size
    self.turn = 1
    self.winner = None
    self.combat_coords = []
    
  def set_player_nums(self):
    for i, player in enumerate(self.players):
      player.set_player_num(i+1)

  def initialize_board(self):
    starting_locations = [(0, mid_x-1), (board_y-1, mid_x-1), (mid_y-1, 0), (mid_y-1, board_x-1)]
    for i, player in enumerate(self.players):
      # starting_coord = (mid_x, (player.player_num-1)*(board_y-1))

      hc = Colony(player.player_num, starting_locations[i], is_hc=True)
      player.home_colony = hc
      self.add_to_board(hc)
      for scout_num in range(3):
        scout = Scout(player.player_num, player.home_colony.coords, scout_num+1)
        self.add_to_board(scout)
        player.ships.append(scout)
      for battlecrusier in range(3):
        bc = Battlecruiser(player.player_num, player.home_colony.coords, battlecrusier+1)
        self.add_to_board(bc)
        player.ships.append(bc)

  def check_if_coords_are_in_bounds(self, coords):
    x, y = coords
    board_x, board_y = self.board_size
    if 1 <= x and x <= board_x:
      if 1 <= y and y <= board_y:
        return True
    return False

  def check_if_translation_is_in_bounds(self, coords, translation):
      max_x, max_y = self.board_size
      x, y = coords
      dx, dy = translation
      new_coords = (x+dx,y+dy)
      return self.check_if_coords_are_in_bounds(new_coords)

  def get_in_bounds_translations(self, coords):
    translations = [(0,0), (0,1), (0,-1), (1,0), (-1,0)]
    in_bounds_translations = []
    for translation in translations:
      if self.check_if_translation_is_in_bounds(coords, translation):
        in_bounds_translations.append(translation)
    return in_bounds_translations

  def movement_phase(self):
    self.log.begin_phase(self.turn, 'MOVEMENT')
    for player in self.players:
      for ship in player.ships:
        if not self.check_for_opponent_ships(player.player_num, ship.coords):
          translations = self.get_in_bounds_translations(ship.coords)
          chosen_move = player.strategy.choose_translation(ship.__dict__, translations)
          orig = ship.coords
          self.move_ship(ship, chosen_move)
          self.log.log_move_ship(ship, orig, ship.coords)
        else:
          if ship.coords not in self.combat_coords:
            self.combat_coords.append(ship.coords)
    self.log.end_phase(self.turn, 'MOVEMENT')
  
  def combat_phase(self):
    self.log.begin_phase(self.turn, 'COMBAT')
    used_coords = []
    for coord in self.combat_coords:
      self.log.log_combat_location(coord)
      sort_cls = sorted(self.all_ships(coord), key=lambda x: x.ship_class)
      for ship in sort_cls:
        if ship.hp == 0:
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
    self.log.end_phase(self.turn, 'COMBAT')

  def check_winner(self):
    for player in self.players:
      opp = self.players[player.get_opponent_player_num()-1]
      for ship in player.ships:
        if ship.coords == opp.home_colony.coords:
          self.winner = player.player_num
  
  def run_to_completion(self, max_turns = 999999999, debug=False):
    self.check_winner
    while self.winner is None and self.turn <= max_turns:
      if debug:
        self.print_board()
      self.movement_phase()
      self.combat_phase()
      self.check_winner()
      self.turn += 1
      if debug:
        self.print_board()
    self.log.player_win(self.winner)

  def add_to_board(self, objs):
    if type(objs) is list:
      for obj in objs:
        coord = obj.coords
        self.board[coord[0]][coord[1]].append(obj)
    else:
      coord = objs.coords
      self.board[coord[0]][coord[1]].append(objs)
    self.update_simple_board()
        
  def remove_from_board(self, objs):
    if type(objs) is list:
      for obj in objs:
        coord = obj.coords
        self.board[coord[0]][coord[1]].remove(obj)
    else:
      coord = objs.coords
      self.board[coord[0]][coord[1]].remove(objs)
    self.update_simple_board()

  def move_ship(self, ship, translation):
    x,y = ship.coords
    new_coords = (x+translation[0], y+translation[1])
    
    try: 
      self.board[new_coords[0]][new_coords[1]]
      self.remove_from_board(ship)
      ship.coords = new_coords
      self.add_to_board(ship)
    except:
      self.log.write('\tInvalid Move, Skipping...\n')

  def check_for_opponent_ships(self, player_num, coords):
    x, y = coords
    for thing in self.board[x][y]:
      if thing.player_num != player_num:
        return True
    return False

  def get_opp_pn(self, player):
    pn = self.players[player.player_num-1].player_num
    if pn == None:
      return None
    elif pn == 1:
      return 2
    elif pn == 2:
      return 1

  def all_objects(self, coord):
    return self.board[coord[0]][coord[1]]

  def all_ships(self, coord):
    return [obj for obj in self.all_objects(coord) if isinstance(obj, Ship)]

  def get_enemies(self, ship, combat_list):
    return [obj for obj in combat_list if obj.player_num != ship.player_num]

  def roll(self):
    return random.randint(1,10)
    
  def hit(self, attacker, defender):
    roll = self.roll()
    atk_value = attacker.atk - defender.df
    if roll <= atk_value:
      return True
    return False
  
  def dead_ship(self, ship):
    player = self.players[ship.player_num - 1]
    player.ships.remove(ship)
    self.remove_from_board(ship)

  def check_coord_for_same_player(self, ship_list):
    return len(set([ship.player_num for ship in ship_list])) == 1

  def print_board(self):
    print('\n')
    for y in range(board_y):
      row_string = ''
      for x in range(board_x):
        if self.board[y][x] == []:
          row_string += '[ ]'
        else:
          print_str = ['{}{}'.format(ship.name[0],ship.player_num) for ship in self.board[y][x] if isinstance(ship, Ship)]
          row_string += str(print_str)
      print(row_string)
    print('\n')

  def dict_to_obj(self, obj_dict, obj_list): #obj list = list that the desired object is in
    for obj in obj_list:
      if obj.name == obj_dict['name']:
        if obj.ship_num == obj_dict['ship_num']:
          if obj.player_num == obj_dict['player_num']:
            return obj
    
  def update_simple_board(self):
    strat_board = {}
    for y_idx in range(len(self.board)):
      for x_idx in range(len(self.board[y_idx])):
        current_loc = self.board[y_idx][x_idx] 
        if len(current_loc) != 0:
          strat_board[(x_idx,y_idx)] = [obj.__dict__ for obj in current_loc]
    for player in self.players:
      player.strategy.simple_board = strat_board
