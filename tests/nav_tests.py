import unittest

import sys
sys.path.append(".")

import hlt
from hlt import Position
from hlt.game_map import GameMap
from util import nav

class TestNav(unittest.TestCase):

    def test_collect_halite(self):
        print (nav.collect_halite(game_map, Position(0, 0)))
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()
