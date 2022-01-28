class Logger:
    def __init__(self, filename='log.txt'):
      self.filename = filename
    
    def clear_log(self):
      with open(self.filename, 'w') as file:
        file.writelines([''])

    def write(self, string=None):
      with open(self.filename, 'a') as file:
        file.writelines([string])

    def initialize(self, players):
      self.write('Begin Game\n')
      for player in players:
        self.write(f'Player {player.player_num} Strategy: {type(player.strategy).__name__}\n')
      
    def begin_phase(self, turn, phase):
      self.write(f'\nBEGIN TURN {turn} {phase} PHASE\n\n')

    def end_phase(self, turn, phase):
      self.write(f'\nEND TURN {turn} {phase} PHASE\n')

    def log_move_ship(self, ship, orig, new):
      self.write(f'\tPlayer {ship.player_num}, {ship.name} {ship.ship_num}: {orig} -> {new}\n')
    
    def log_combat_location(self, coords):
      self.write(f'\tCombat at: {coords}\n\n')
          
    def combat_ships(self, attacker, defender):
      self.write(f'\t\tAttacker: Player {attacker.player_num} {attacker.name} {attacker.ship_num}\n')
      self.write(f'\t\tDefender: Player {defender.player_num} {defender.name} {defender.ship_num}\n')
    
    def ship_hit(self, attacker, defender, dmg):
      self.write(f'\t\tPlayer {attacker.player_num} {attacker.name} {attacker.ship_num} dealt {dmg} dmg to Player {defender.player_num} {defender.name} {defender.ship_num}\n\n')

    def ship_destroyed(self, ship):
      self.write(f'\t\tPlayer {ship.player_num} {ship.name} {ship.ship_num} was destroyed\n\n')

    def player_win(self, winner_num):
      self.write(f'\nWinner: Player {winner_num}')
