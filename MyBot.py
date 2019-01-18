#!/usr/bin/env python3

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

while len(game.me.get_ships()) < 10:
    explore_strategy(game, ship_status, cells)

while True:
    destination_strategy(game, sections_exploring, ship_destinations, ship_status, cells)