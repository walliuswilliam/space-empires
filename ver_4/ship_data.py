import sys
sys.path.append('ver_4/objects')
from ships import *

scout = {'hp': 1, 'atk': 3, 'df': 0, 'name': 'Scout', 'ship_class': 'E', 'cp_cost': 6, 'maint_cost': 1}
battlecruiser = {'hp': 2, 'atk': 5, 'df': 1, 'name': 'BattleCruiser', 'ship_class': 'B', 'cp_cost': 15, 'maint_cost': 2}
battleship = {'hp': 3, 'atk': 5, 'df': 2, 'name': 'Battleship', 'ship_class': 'A', 'cp_cost': 20, 'maint_cost': 3}
cruiser = {'hp': 2, 'atk': 4, 'df': 1, 'name': 'Cruiser', 'ship_class': 'C', 'cp_cost': 12, 'maint_cost': 2}
destroyer = {'hp': 1, 'atk': 4, 'df': 0, 'name': 'Destroyer', 'ship_class': 'D', 'cp_cost': 9, 'maint_cost': 1}
dreadnaught = {'hp': 3, 'atk': 6, 'df': 3, 'name': 'Dreadnaught', 'ship_class': 'A', 'cp_cost': 24, 'maint_cost': 3}

all_ships = [scout, battlecruiser, battleship, cruiser, destroyer, dreadnaught]
ship_objects = {'Scout': Scout, 'BattleCruiser': BattleCruiser, 'Battleship': Battleship, 'Cruiser': Cruiser, 'Destroyer': Destroyer, 'Dreadnaught':Dreadnaught}