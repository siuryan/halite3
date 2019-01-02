import hlt
from hlt import constants
from hlt import Direction
from hlt import Position

def check_sparse(game_map, position):
    surroundings = position.get_surrounding_cardinals()
    halite_amounts = list(map(lambda pos: game_map[pos].halite_amount, surroundings))

    if max(halite_amounts) < constants.MAX_HALITE/20:
        return True

    return False

def collect_halite(game_map, position):
    surroundings = position.get_surrounding_cardinals()
    halite_amounts = list(map(lambda pos: game_map[pos].halite_amount, surroundings))

    if max(halite_amounts) - .1 * game_map[position].halite_amount > game_map[position].halite_amount:
        return surroundings[halite_amounts.index(max(halite_amounts))]

    return Position(0, 0)

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

'''
def naive_navigate_no_shipyard(game_map, ship, destination):
    for direction in game_map.get_unsafe_moves(ship.position, destination):
        target_pos = ship.position.directional_offset(direction)
        if game_map[target_pos].has_structure:
            return
        if not game_map[target_pos].is_occupied and game_map[target_pos].has_structure:
            game_map[target_pos].mark_unsafe(ship)
            return direction

    return Direction.Still
'''
