import random

import hlt
from hlt import constants
from hlt import Direction
from hlt import Position

def check_inspiration(game_map, me, position):
    cells = [item for sublist in game_map._cells for item in sublist]
    surroundings = filter(lambda x: game_map.calculate_distance(position, x.position) <= 4, cells)

    for cell in surroundings:
        if cell.ship and cell.ship.owner != me.id:
            return True
    return False

def collect_halite(game_map, me, ship):
    surroundings = ship.position.get_surrounding_cardinals()
    halite_amounts = list(map(
        lambda pos: game_map[pos].halite_amount * 3 if check_inspiration(game_map, me, pos) else game_map[pos].halite_amount, surroundings
    ))

    current_cell_halite_amount = game_map[ship.position].halite_amount * 3 if check_inspiration(game_map, me, ship.position) else game_map[ship.position].halite_amount
    if max(halite_amounts) - .1 * game_map[ship.position].halite_amount > current_cell_halite_amount:
        return surroundings[halite_amounts.index(max(halite_amounts))]

    if current_cell_halite_amount == 0:
        return ship.position.directional_offset([Direction.North, Direction.South, Direction.East, Direction.West][random.randint(0, 3)])
    return ship.position

def should_collapse(game_map, ship, shipyard, turn):
    return game_map.calculate_distance(ship.position, shipyard.position) + game_map.width / 3 >= constants.MAX_TURNS - turn

def random_direction():
    return random.choice([Direction.North, Direction.South, Direction.East, Direction.West])

def should_spawn(game, me, density, turn):
    return turn < 150 or (density > constants.HALITE_DENSITY_THRESHOLD and turn < 200) or \
    (turn < constants.MAX_TURNS - 100 and len(game.players) == 2 and len(me.get_ships()) < max([len(game.players[player].get_ships()) for player in game.players])) or \
    (turn < constants.MAX_TURNS * .6 and len(game.players) == 4)
