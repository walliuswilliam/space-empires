from logger import *

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

    def log_move_ship(self, player_id, ship_name, orig, new):
      self.write('\tPlayer {}, {}: {} -> {}\n'.format(player_id,ship_name,orig,new))
    
    def log_combat_location(self, coords):
      self.write('\tCombat at: {}\n'.format(coords))
          
    def combat_ships(self, attacker, defender):
      self.write('\n\t\t')
      self.write('Attacker: Player {} {}'.format(attacker.player_num, attacker.name))

      self.write('\n\t\t')
      self.write('Defender: Player {} {}'.format(defender.player_num, defender.name))
    
    def ship_hit(self, attacker, defender, dmg):
      self.write('\n\t\tPlayer {} {} dealt {} dmg to Player {} {}\n'.format(attacker.player_num, attacker.name, dmg, defender.player_num, defender.name))

    def ship_destroyed(self, ship):
      self.write('\t\tPlayer {} {} was destroyed\n'.format(ship.player_num, ship.name))


    def player_win(self, winner_num):
      self.write('\nWinner: Player {}'.format(winner_num))



      # if hit == 1 :
      #   self.write('\n\t\tHit!')
      #   line = 'Player {} Scout {} was destroyed'.format(defender[0],defender[1])
      # else :
      #   line = '(Miss)'
      # self.write('\n\t\t')
      # self.write(line)
      # self.write('\n')
            
    def log_survivors(self, battle_survivors) :
      if battle_survivors != {} :
        self.write('\n\tSurvivors:')
      for (battle, survivors) in battle_survivors.items() :
        self.write('\n\n\t\t')
        self.write(str(battle))
        self.write('\n')
        for (p_id, scout_id) in survivors :
          self.write('\n\t\t\t')
          self.write('Player {} Scout {}'.format(p_id, scout_id))