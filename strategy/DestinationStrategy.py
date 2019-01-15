#!/usr/bin/env python3

import random
import logging

# Import the Halite SDK, which will let you interact with the game.
import hlt
from hlt import constants
from hlt.entity import Ship

from util import nav
from util import map_sections

from strategy import common

def destination_strategy(game):

    sections_exploring = []
    for i in range(0, 8):
        sections_exploring.append([-1, -1, -1, -1, -1, -1, -1, -1])

    ship_destinations = {}
    ship_status = {}

    cells = [item for sublist in game.game_map._cells for item in sublist]

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

        for ship in me.get_ships():
            logging.info("Ship {} has {} halite.".format(ship.id, ship.halite_amount))
            logging.info("Ship {} is {}.".format(ship.id, ship_status[ship.id] if ship.id in ship_status else "no status"))

            if nav.should_collapse(game_map, ship, me.shipyard, game.turn_number):
                ship_status[ship.id] = "collapse"

            if ship.id not in ship_status:
                # Send it to the most optimal section of the map
                max_dest_info = map_sections.max_dest(map_sections.get_section_values(ship, game_map, game.turn_number), sections_exploring, game_map.width, game_map.height, me.shipyard.position)
                ship_destinations[ship.id] = game_map.normalize(max_dest_info[0])
                ship.destx = max_dest_info[1]
                ship.desty = max_dest_info[2]
                sections_exploring[ship.destx][ship.desty] = ship.id
                ship_status[ship.id] = "deploying"

            if ship_status[ship.id] == "collapse":
                common.collapse(game, me, command_queue, ship)
                continue

            if ship_status[ship.id] != "returning" and ship.halite_amount >= constants.MAX_HALITE * .9:
                ship_status[ship.id] = "returning"

            if ship_status[ship.id] == "returning" and ship.halite_amount >= game_map[ship.position].halite_amount * 0.1:
                if ship.position == me.shipyard.position:
                    # Re-deploy it to an optimal section of the map
                    sections_exploring[ship.destx][ship.desty] = -1
                    max_dest_info = map_sections.max_dest(map_sections.get_section_values(ship, game_map, game.turn_number), sections_exploring, game_map.width, game_map.height, me.shipyard.position)
                    ship_destinations[ship.id] = game_map.normalize(max_dest_info[0])
                    ship.destx = max_dest_info[1]
                    ship.desty = max_dest_info[2]
                    sections_exploring[ship.destx][ship.desty] = ship.id
                    ship_status[ship.id] = "deploying"
                else:
                    #move = nav.returning(game_map, ship, me.shipyard)
                    move = game_map.naive_navigate(ship, me.shipyard.position)
                    continue

            # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
            #   Else, collect halite.
            if (game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full) and ship.halite_amount >= game_map[ship.position].halite_amount * 0.1:
                if ship_status[ship.id] == "deploying":
                    logging.info(ship_destinations[ship.id])
                    if ship.position == me.shipyard.position:
                        #move = nav.exiting(game_map, ship, me.shipyard, ship_destinations[ship.id])
                        move = game_map.naive_navigate(ship, ship_destinations[ship.id])
                    elif ship.position == ship_destinations[ship.id]:
                        ship_status[ship.id] = "exploring"
                    else:
                        move = game_map.naive_navigate(ship, ship_destinations[ship.id])
                if ship_status[ship.id] == "exploring":
                    '''
                    if nav.check_sparse(game_map, ship.position):
                        sections_exploring[ship.destx][ship.desty] = -1
                        max_dest_info = map_sections.max_dest(map_sections.get_section_values(ship, game_map, game.turn_number), sections_exploring, game_map.width, game_map.height, me.shipyard.position)
                        ship_destinations[ship.id] = game_map.normalize(max_dest_info[0])
                        ship.destx = max_dest_info[1]
                        ship.desty = max_dest_info[2]
                        sections_exploring[ship.destx][ship.desty] = ship.id
                        ship_status[ship.id] = "deploying"
                        if
                        move = game_map.naive_navigate(ship, ship_destinations[ship.id])
                    else:
                    '''
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

        common.handle_commands(game, me, command_queue)

        # If you're on the first turn and have enough halite, spawn a ship.
        # Don't spawn a ship if you currently have a ship at port, though.
        common.spawn_ship(game, me, command_queue, cells)

        logging.info(command_queue)

        # Send your moves back to the game environment, ending this turn.
        game.end_turn(command_queue)
