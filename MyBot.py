#!/usr/bin/env python3

import random
import logging

# Import the Halite SDK, which will let you interact with the game.
import hlt
from hlt import constants

from util import nav
from util import map_sections

# This game object contains the initial game state.
game = hlt.Game()

me = game.me
game_map = game.game_map

sections_exploring = []
for i in range(0, 8):
    sections_exploring.append([-1, -1, -1, -1, -1, -1, -1, -1])

section_values = map_sections.get_section_values(me, game_map)

# Respond with your name.
game.ready("v1")

ship_destinations = {}
ship_status = {}

while True:
    # Get the latest game state.
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map

    # A command queue holds all the commands you will run this turn.
    command_queue = []

    for ship in me.get_ships():
        logging.info("Ship {} has {} halite.".format(ship.id, ship.halite_amount))

        if ship.id not in ship_status:
            # Send it to the most optimal section of the map
            max_dest_info = map_sections.max_dest(section_values, map_sections.get_section_values(me, game_map), game_map.width, game_map.height)
            ship_destinations[ship.id] = max_dest_info[0]
            ship.destx = max_dest_info[1]
            ship.desty = max_dest_info[2]
            sections_exploring[ship.destx][ship.desty] = ship.id
            ship_status[ship.id] = "deploying"

        if ship_status[ship.id] == "returning":
            if ship.position == me.shipyard.position:
                # Re-deploy it to an optimal section of the map
                sections_exploring[ship.destx][ship.desty] = -1
                max_dest_info = map_sections.max_dest(section_values, map_sections.get_section_values(me, game_map), game_map.width, game_map.height)
                ship_destinations[ship.id] = max_dest_info[0]
                ship.destx = max_dest_info[1]
                ship.desty = max_dest_info[2]
                sections_exploring[ship.destx][ship.desty] = ship.id
                ship_status[ship.id] = "deploying"
            else:
                move = nav.returning(game_map, ship, me.shipyard)
                command_queue.append(ship.move(move))
                continue
        elif ship.halite_amount >= constants.MAX_HALITE * .9:
            ship_status[ship.id] = "returning"

        # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
        #   Else, collect halite.
        if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full:
            if ship_status[ship.id] == "deploying":
                logging.info(ship_destinations[ship.id])
                if ship.position == me.shipyard.position:
                    move = nav.exiting(game_map, ship, me.shipyard, ship_destinations[ship.id])
                    command_queue.append(ship.move(move))
                elif ship.position == ship_destinations[ship.id]:
                    ship_status[ship.id] = "exploring"
                else:
                    move = game_map.naive_navigate(ship, ship_destinations[ship.id])
                    command_queue.append(ship.move(move))
            if ship_status[ship.id] == "exploring":
                move = game_map.naive_navigate(ship, nav.collect_halite(game_map, ship.position))
                command_queue.append(ship.move(move))
        else:
            command_queue.append(ship.stay_still())

    # If you're on the first turn and have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though.
    if game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST and (not game_map[me.shipyard].is_occupied or (game_map[me.shipyard].is_occupied and game_map[me.shipyard].ship.owner != me.id)):
        command_queue.append(me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)
