class Ship():
  def func():
    return None

class Scout(Ship):
  def __init__(self, player_number, coords, ship_num):
    self.name = 'Scout'
    self.cls = 'E'
    self.atk = 3
    self.df = 0
    self.hp = 1
    self.player_num = player_number
    self.coords = coords
    self.ship_num = ship_num

class Battlecruiser(Ship):
  def __init__(self, player_number, coords, ship_num):
    self.name = 'Battlecruiser'
    self.cls = 'B'
    self.atk = 5
    self.df = 1
    self.hp = 2
    self.player_num = player_number
    self.coords = coords
    self.ship_num = ship_num
