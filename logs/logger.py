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
    
    def log_movement(self, player_id, scout_id, start, stop) :
      self.write('\n\t')
      self.write('Player {} Scout {}: {} -> {}'.format(player_id,scout_id,start,stop))
      #I personally like "Player {}, Scout {}: {} -->  but go off

    def begin_phase(self, turn, phase) :
      #Personally like 'BEGIN TURN {} {} PHASE' 
      self.write('BEGINNING OF TURN {} {} PHASE'.format(turn, phase))

    def end_phase(self, turn, phase) :
      self.write('\n\n')
      #still like this... 'END TURN {} {} PHASE'
      self.write('END OF TURN {} {} PHASE'.format(turn, phase))
      self.write('\n\n')
    
    def log_combat_locations(self, battles) :
      if battles != {} :
        self.write('\n\n\tCombat Locations:')
      for (coords, fighters) in battles.items() :
        self.write('\n\n\t\t')
        self.write(str(coords))
        self.write('\n')
        for (p_id,scout_id) in fighters :
          self.write('\n\t\t\t')
          self.write('Player {} Scout {}'.format(p_id,scout_id))
        if battles != {} :
          self.write('\n')
    
    def log_combat(self, attacker, defender, hit) :
      self.write('\n\t\t')
      self.write('Attacker: Player {} Scout {}'.format(attacker[0],attacker[1]))

      self.write('\n\t\t')
      self.write('Defender: Player {} Scout {}'.format(defender[0],defender[1]))

      if hit == 1 :
        self.write('\n\t\tHit!')
        line = 'Player {} Scout {} was destroyed'.format(defender[0],defender[1])
      else :
        line = '(Miss)'
      self.write('\n\t\t')
      self.write(line)
      self.write('\n')
            
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