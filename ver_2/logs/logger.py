class Logger:
    def __init__(self, filename='log.txt'):
      self.filename = filename
    
    def clear_log(self):
      with open(self.filename, 'w') as file:
        file.writelines([''])

    def write(self, string=None):
      with open(self.filename, 'a') as file:
        file.writelines([string])

    def begin_phase(self, turn, phase):
      self.write('\nBEGIN TURN {} {} PHASE\n\n'.format(turn, phase))

    def end_phase(self, turn, phase):
      self.write('\nEND TURN {} {} PHASE\n'.format(turn, phase))

    def log_move_ship(self, ship, orig, new):
      self.write('\tPlayer {}, {} {}: {} -> {}\n'.format(ship.player_num,ship.name,ship.ship_num,orig,new))
    
    def log_combat_location(self, coords):
      self.write('\tCombat at: {}\n'.format(coords))
          
    def combat_ships(self, attacker, defender):
      self.write('\n\t\t')
      self.write('Attacker: Player {} {} {}'.format(attacker.player_num, attacker.name, attacker.ship_num))

      self.write('\n\t\t')
      self.write('Defender: Player {} {} {}'.format(defender.player_num, defender.name, defender.ship_num))
    
    def ship_hit(self, attacker, defender, dmg):
      self.write('\n\t\tPlayer {} {} {} dealt {} dmg to Player {} {} {}\n'.format(attacker.player_num, attacker.name,attacker.ship_num, dmg, defender.player_num, defender.name, defender.ship_num))

    def ship_destroyed(self, ship):
      self.write('\t\tPlayer {} {} {} was destroyed\n'.format(ship.player_num, ship.name, ship.ship_num))

    def player_win(self, winner_num):
      self.write('\nWinner: Player {}'.format(winner_num))
