#!/usr/bin/env python3

from functools import reduce

# Import the Halite SDK, which will let you interact with the game.
import hlt
import logging

from strategy.CombinedStrategy import combined_strategy

# This game object contains the initial game state.
game = hlt.Game()

me = game.me
game_map = game.game_map

cells = [item.halite_amount for sublist in game_map._cells for item in sublist]
map_density = reduce(lambda total, halite: total + halite, cells) / len(cells) # spawn number of ships based on this

combined_strategy(game)