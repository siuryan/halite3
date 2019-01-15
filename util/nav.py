import random

import hlt
from hlt import constants
from hlt import Direction
from hlt import Position

def check_sparse(game_map, position):
    surroundings = position.get_surrounding_cardinals()
    halite_amounts = list(map(lambda pos: game_map[pos].halite_amount, surroundings))

    if max(halite_amounts) < constants.MAX_HALITE/10:
        return True

    return False

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
        return ship.position.directional_offset([Direction.North, Direction.South, Direction.East, Direction.West][random.randint(0, 4)])
    return ship.position

def returning(game_map, ship, shipyard):
    if ship.position.y == shipyard.position.y:
        direction = game_map.naive_navigate(ship, ship.position + Position(0, 1))
        if direction != Direction.Still:
            return direction
        return game_map.naive_navigate(ship, ship.position + Position(0, -1))
    if game_map.calculate_distance(shipyard.position, ship.position) == 1:
        return game_map.naive_navigate(ship, shipyard.position)

    n_entrance = shipyard.position + Position(0, 1)
    s_entrance = shipyard.position + Position(0, -1)

    if game_map.calculate_distance(n_entrance, ship.position) < game_map.calculate_distance(s_entrance, ship.position):
        return game_map.naive_navigate(ship, n_entrance)

    return game_map.naive_navigate(ship, s_entrance)

def exiting(game_map, ship, shipyard, destination):
    w_exit = shipyard.position + Position(-1, 0)
    e_exit = shipyard.position + Position(1, 0)
    if game_map.calculate_distance(w_exit, destination) < game_map.calculate_distance(e_exit, destination):
        return game_map.naive_navigate(ship, w_exit)
    return game_map.naive_navigate(ship, e_exit)

def should_collapse(game_map, ship, shipyard, turn):
    return game_map.calculate_distance(ship.position, shipyard.position) + game_map.width / 3 >= constants.MAX_TURNS - turn

def random_direction():
    return random.choice([Direction.North, Direction.South, Direction.East, Direction.West])

def should_spawn(density):
    return constants.HALITE_DENSITY_THRESHOLD
