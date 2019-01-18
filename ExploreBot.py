#!/usr/bin/env python3

# Import the Halite SDK, which will let you interact with the game.
import hlt

from strategy.ExploreStrategy import run_explore_strategy 

# This game object contains the initial game state.
game = hlt.Game()

run_explore_strategy(game)