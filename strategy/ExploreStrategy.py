#!/usr/bin/env python3

import random
import logging
from functools import reduce

# Import the Halite SDK, which will let you interact with the game.
import hlt
from hlt import constants
from hlt.entity import Ship

from util import nav
from util import map_sections

from strategy import common

def explore_strategy(game):
    
    ship_status = {}

    # Respond with your name.
    game.ready("v1")

    while True:
        # Get the latest game state.
        game.update_frame()
        # You extract player metadata and the updated map metadata here for convenience.
        me = game.me
        game_map = game.game_map

        # A command queue holds all the commands you will run this turn.
        command_queue = []
        Ship.next_move_squares = {}

        cells = [item for sublist in game_map._cells for item in sublist]

        for ship in me.get_ships():
            logging.info("Ship {} has {} halite.".format(ship.id, ship.halite_amount))
            logging.info("Ship {} is {}.".format(ship.id, ship_status[ship.id] if ship.id in ship_status else "no status"))

            if nav.should_collapse(game_map, ship, me.shipyard, game.turn_number):
                ship_status[ship.id] = "collapse"

            if ship.id not in ship_status:
                ship_status[ship.id] = "exploring"

            if ship_status[ship.id] == "collapse":
                common.collapse(game, me, command_queue, ship)
                continue

            if ship_status[ship.id] != "returning" and ship.halite_amount >= constants.MAX_HALITE * .65:
                ship_status[ship.id] = "returning"

            if ship_status[ship.id] == "returning" and ship.halite_amount >= game_map[ship.position].halite_amount * 0.1:
                if ship.position == me.shipyard.position:
                    ship_status[ship.id] = "exploring"
                else:
                    move = game_map.naive_navigate(ship, me.shipyard.position)
                    continue

            # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
            #   Else, collect halite.
            if (game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full) and ship.halite_amount >= game_map[ship.position].halite_amount * 0.1:
                if ship_status[ship.id] == "exploring":
                    position = nav.collect_halite(game_map, me, ship)
                    if position == ship.position:
                        if game_map.normalize(ship.position) in Ship.next_move_squares:
                            Ship.next_move_squares[game_map.normalize(ship.position)].insert(0, ship)
                        else:
                            Ship.next_move_squares[game_map.normalize(ship.position)] = [ship]
                        continue
                    move = game_map.naive_navigate(ship, position)
            else:
                #add to the dictionary
                if game_map.normalize(ship.position) in Ship.next_move_squares:
                    Ship.next_move_squares[game_map.normalize(ship.position)].insert(0, ship)
                else:
                    Ship.next_move_squares[game_map.normalize(ship.position)] = [ship]

        for position in Ship.next_move_squares:
            logging.info(Ship.next_move_squares)
            logging.info(position)
            ship = Ship.next_move_squares[position][0]
            logging.info(ship)
            if ship.position == position:
                move = 'o'
            else:
                move = game_map.get_unsafe_moves(ship.position, position)[0]
                command_queue.append(ship.move(move))
            if len(Ship.next_move_squares[position]) > 1:
                for ship in Ship.next_move_squares[position][1:]:
                    logging.info(ship.id)
                    Ship.next_move_squares[position].remove(ship)
                    move = game_map.naivest_navigate(ship, nav.collect_halite(game_map, me, ship))
                    logging.info(move)
                    command_queue.append(ship.move(move))

        # If you're on the first turn and have enough halite, spawn a ship.
        # Don't spawn a ship if you currently have a ship at port, though.
        common.spawn_ship(game, me, command_queue, cells)

        logging.info(command_queue)

        # Send your moves back to the game environment, ending this turn.
        game.end_turn(command_queue)
