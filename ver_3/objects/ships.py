class Battlecruiser:
  def __init__(self, player_number, coords, ship_num):
    self.name = 'BattleCruiser'
    self.ship_class = 'B'
    self.atk = 5
    self.df = 1
    self.hp = 2
    self.cp_cost = 15
    self.player_num = player_number
    self.coords = coords
    self.ship_num = ship_num
    self.obj_type = 'Ship'

class Battleship:
  def __init__(self, player_number, coords, ship_num):
    self.name = 'Battleship'
    self.ship_class = 'A'
    self.atk = 5
    self.df = 2
    self.hp = 3
    self.cp_cost = 20
    self.player_num = player_number
    self.coords = coords
    self.ship_num = ship_num
    self.obj_type = 'Ship'

class Cruiser:
  def __init__(self, player_number, coords, ship_num):
    self.name = 'Cruiser'
    self.ship_class = 'C'
    self.atk = 4
    self.df = 1
    self.hp = 2
    self.cp_cost = 12
    self.player_num = player_number
    self.coords = coords
    self.ship_num = ship_num
    self.obj_type = 'Ship'

class Destroyer:
  def __init__(self, player_number, coords, ship_num):
    self.name = 'Destroyer'
    self.ship_class = 'D'
    self.atk = 4
    self.df = 0
    self.hp = 1
    self.cp_cost = 9
    self.player_num = player_number
    self.coords = coords
    self.ship_num = ship_num
    self.obj_type = 'Ship'

class Dreadnaught:
  def __init__(self, player_number, coords, ship_num):
    self.name = 'Dreadnaught'
    self.ship_class = 'A'
    self.atk = 6
    self.df = 3
    self.hp = 3
    self.cp_cost = 24
    self.player_num = player_number
    self.coords = coords
    self.ship_num = ship_num
    self.obj_type = 'Ship'

class Scout:
  def __init__(self, player_number, coords, ship_num):
    self.name = 'Scout'
    self.ship_class = 'E'
    self.atk = 3
    self.df = 0
    self.hp = 1
    self.cp_cost = 6
    self.player_num = player_number
    self.coords = coords
    self.ship_num = ship_num
    self.obj_type = 'Ship'
