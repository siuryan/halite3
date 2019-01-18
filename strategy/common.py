from functools import reduce

import hlt
import logging
from hlt import constants
from hlt.entity import Ship

from util import nav

def collapse(game, me, command_queue, ship):
    if game.game_map.calculate_distance(ship.position, me.shipyard.position) == 1:
        move = game.game_map.get_unsafe_moves(ship.position, me.shipyard.position)[0]
        command_queue.append(ship.move(move))
    else:
        move = game.game_map.naivest_navigate(ship, me.shipyard.position)
        command_queue.append(ship.move(move))


def spawn_ship(game, me, command_queue, cells):
    halites = [cell.halite_amount for cell in cells]
    map_density = reduce(lambda total, halite: total + halite, halites) / len(cells)

    if nav.should_spawn(game, me, map_density, game.turn_number) and \
        me.halite_amount >= constants.SHIP_COST and (not game.game_map[me.shipyard].is_occupied or \
        (game.game_map[me.shipyard].is_occupied and game.game_map[me.shipyard].ship.owner != me.id)):
        command_queue.append(me.shipyard.spawn())

def handle_commands(game, me, command_queue):
    for position in Ship.next_move_squares:
        logging.info(Ship.next_move_squares)
        logging.info(position)
        first_ship = Ship.next_move_squares[position][0]
        if len(Ship.next_move_squares[position]) > 1:
            for ship in Ship.next_move_squares[position]:
                if ship.position == position:
                    first_ship = ship
                    break

        logging.info(first_ship)
        if first_ship.position == position:
            move = 'o'
        else:
            move = game.game_map.get_unsafe_moves(first_ship.position, position)[0]
        command_queue.append(first_ship.move(move))
        for ship in Ship.next_move_squares[position][1:]:
            logging.info(ship.id)
            Ship.next_move_squares[position].remove(ship)
            move = game.game_map.naiver_navigate(ship, nav.collect_halite(game.game_map, me, ship))
            logging.info(move)
            command_queue.append(ship.move(move))
