import unittest

from level import *
from tileComponents import UNCOVERED, COVERED, NORTH_FACING_PLANE, WEST_FACING_PLANE, SOUTH_FACING_PLANE, EAST_FACING_PLANE
from board import BoardObjective, PathObjective

class TestLevelMethods(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
