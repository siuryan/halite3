from functools import reduce

import hlt
from hlt import constants

from util import nav

def collapse(game, me, command_queue, ship):
    if game.game_map.calculate_distance(ship.position, me.shipyard.position) == 1:
        move = game.game_map.get_unsafe_moves(ship.position, me.shipyard.position)[0]
        command_queue.append(ship.move(move))

    move = game.game_map.naivest_navigate(ship, me.shipyard.position)
    command_queue.append(ship.move(move))


def spawn_ship(game, me, command_queue, cells):
    halites = [cell.halite_amount for cell in cells]
    map_density = reduce(lambda total, halite: total + halite, halites) / len(cells)

    if nav.should_spawn(map_density) and game.turn_number <= 200 and \
        me.halite_amount >= constants.SHIP_COST and (not game.game_map[me.shipyard].is_occupied or \
        (game.game_map[me.shipyard].is_occupied and game.game_map[me.shipyard].ship.owner != me.id)):
        command_queue.append(me.shipyard.spawn())