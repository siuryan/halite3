#!/usr/bin/env python3

import random
import logging

# Import the Halite SDK, which will let you interact with the game.
import hlt
from hlt import constants

from util import nav

# This game object contains the initial game state.
game = hlt.Game()

me = game.me
game_map = game.game_map
section_values = [ [], [], [], [], [], [], [], [] ]
for x in range(0, 8):
    for y in range(0, 8):
        section_values[x].append(0)
        start_x = x * game_map.width / 8
        start_y = y * game_map.height / 8
        end_x = (x + 1) * game_map.width / 8
        end_y = (y + 1) * game_map.height / 8
        for section_x in range(start_x, end_x):
            for section_y in range(start_y, end_y):
                section_values[x][y] += 1.0 * (game_map[Position(section_x, section_y)].halite_amount) / game_map.calculate_distance(me.shipyard.position, Position(section_x, section_y))



# Respond with your name.
game.ready("StarterBot")

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
            ship_status[ship.id] = "exploring"

        if ship_status[ship.id] == "returning":
            if ship.position == me.shipyard.position:
                ship_status[ship.id] = "exploring"
            else:
                move = game_map.naive_navigate(ship, me.shipyard.position)
                command_queue.append(ship.move(move))
                continue
        elif ship.halite_amount >= constants.MAX_HALITE * .9:
            ship_status[ship.id] = "returning"

        # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
        #   Else, collect halite.
        if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full:
            command_queue.append(ship.move(nav.collect_halite(game_map, ship.position)))
        else:
            command_queue.append(ship.stay_still())

    # If you're on the first turn and have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though.
    if game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(game.me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)
