import sys
import random as rand
import math

sys.path.append('logs')
from ships import *
from players import *
from logger import *
from colony import *


class Game:
  def __init__(self, players, random_seed=None, board_size=[7,7]):
    self.players = players
    self.set_player_nums()
    self.log = Logger('logs/log.txt')
    self.log.clear_log()

    rand.seed(random_seed)

    global board_x,board_y, mid_x, mid_y

    board_x, board_y = board_size
    mid_x = (board_x + 1) // 2
    mid_y = (board_y + 1) // 2

    self.board = [[[] for _ in range(board_x)] for _ in range(board_y)]

    self.place_ships()
    print(self.board)

    for i in range(3):
      p1 = Scout(1,(mid_x,1))
      self.board[mid_x][1].append(p1)
      self.players[0].ships.append(p1)
      p2 = Scout(2,(mid_x,7))
      self.board[mid_x][board_x-1].append(p2)
      self.players[1].ships.append(p2)
    
    self.board_size = board_size
    self.turn = 1
    self.winner = None
    
  def set_player_nums(self):
    for i, player in enumerate(self.players):
      player.set_player_num(i+1)

  def place_ships(self):
    starting_locations = [(0, mid_x-1), (board_y-1, mid_x-1), (mid_y-1, 0), (mid_y-1, board_x-1)]
    for i, player in enumerate(self.players):
      hc = HomeColony(player.player_num, starting_locations[i])
      player.home_colony = hc
      self.add_to_board(hc)
    for scout_num in range(3):
      scout = Scout(player.player_num, player.home_colony.coords)


      
      
      # for i in range(3):
        
      #   Scout()
      # for i in range(1):






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

  def complete_movement_phase(self):
    self.log.write('\nBEGINNING OF TURN {} MOVEMENT PHASE\n\n'.format(self.turn))
    for player in self.players:
      print('player', player.player_num)
      for ship in player.ships:
        # print(self.board[ship.coords[0]][ship.coords[1]]) NEED TO IMPLEMENT SHIPS NOT MOVING OFF SPACE IF ENEMY SHIPS ARE ON
        # if len(self.board[ship.coords[0]][ship.coords[1]]) == 1:
        translations = self.get_in_bounds_translations(ship.coords)
        chosen_move = player.choose_translation(self.board, translations, ship, self.players[self.get_opp_pn(player)-1].home_colony)
        print('pre ship coords', ship.coords)
        self.move_ship(ship, chosen_move)
        print('post ship coords', ship.coords)


  def add_to_board(self, objs):
    if type(objs) is list:
      for obj in objs:
        coord = obj.coords
        self.board[coord[1]][coord[0]].append(obj)
    else:
      coord = objs.coords
      self.board[coord[1]][coord[0]].append(objs)
        
  def remove_from_board(self, objs):
    if type(objs) is list:
      for obj in objs:
        coord = obj.coords
        self.board[coord[1]][coord[0]].remove(obj)
    else:
      coord = objs.coords
      self.board[coord[1]][coord[0]].remove(objs)

  def move_ship(self, ship, translation):
    x,y = ship.coords
    new_coords = (x+translation[0], y+translation[1])
    self.remove_from_board(ship)
    self.add_to_board(ship)
    ship.coords = new_coords

  def check_for_opponent_ships(self, player_num, coords):
    x, y = coords
    for thing in self.board[x][y]:
      if thing.player_num != player_num:
        return False
    return True

  def get_opp_pn(self, player):
    pn = self.players[player.player_num-1].player_num
    if pn == None:
      return None
    elif pn == 1:
      return 2
    elif pn == 2:
      return 1