#!/usr/bin/env python3

from functools import reduce

# Import the Halite SDK, which will let you interact with the game.
import hlt
import logging

from strategy.DestinationStrategy import run_destination_strategy

# This game object contains the initial game state.
game = hlt.Game()

run_destination_strategy(game)