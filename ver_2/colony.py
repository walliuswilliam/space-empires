class Colony:
  def __init__(self, player_number, coords, is_hc=False):
    self.coords = coords
    self.player_num = player_number
    self.is_home_colony = is_hc
    self.obj_type = 'Colony'