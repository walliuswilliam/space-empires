class Ship():
  def func():
    return None

class Scout(Ship):
  def __init__(self, player_number, coords):
    self.name = 'Scout'
    self.cls = 'E'
    self.atk = 3
    self.df = 0
    self.hp = 1
    self.player_num = player_number
    self.coords = coords

class Battlecruiser(Ship):
  def __init__(self, player_number, coords):
    self.name = 'Battlecruiser'
    self.cls = 'B'
    self.atk = 5
    self.df = 1
    self.hp = 2
    self.player_num = player_number
    self.coords = coords
