#!/usr/bin/env python3
from functools import reduce

# Import the Halite SDK, which will let you interact with the game.
import hlt

from strategy.ExploreStrategy import explore_strategy
from strategy.DestinationStrategy import destination_strategy

# This game object contains the initial game state.
game = hlt.Game()


sections_exploring = []
for i in range(0, 8):
    sections_exploring.append([-1, -1, -1, -1, -1, -1, -1, -1])

ship_destinations = {}
ship_status = {}

cells = [item for sublist in game.game_map._cells for item in sublist]

# Respond with your name.
game.ready("MyBot")

while True:
    halites = [cell.halite_amount for cell in cells]
    map_density = reduce(lambda total, halite: total + halite, halites) / len(cells)

    if len(game.me.get_ships()) < 10 or map_density < hlt.constants.HALITE_DENSITY_THRESHOLD or (len(game.players) == 4 and game.game_map.width <= 40):
        explore_strategy(game, ship_status, cells)

    else:
        destination_strategy(game, sections_exploring, ship_destinations, ship_status, cells)