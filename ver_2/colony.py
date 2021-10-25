class Colony:
  def __init__(self, player_number, coords):
    self.coords = coords
    self.player_num = player_number
    self.is_home_colony = False
    self.obj_type = 'Colony'