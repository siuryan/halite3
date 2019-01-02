import hlt
from hlt import constants
from hlt import Direction
from hlt import Position

def collect_halite(game_map, position):
    surroundings = position.get_surrounding_cardinals()
    halite_amounts = list(map(lambda pos: game_map[pos].halite_amount, surroundings))

    if max(halite_amounts) - .1 * game_map[position].halite_amount > game_map[position].halite_amount:
        return surroundings[halite_amounts.index(max(halite_amounts))]

    return Position(0, 0)
