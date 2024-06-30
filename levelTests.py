import unittest

from cardinalDirections import SOUTH, NORTH, WEST, EAST
from level import *
from tileComponents import UNCOVERED, COVERED, NORTH_FACING_PLANE, \
    WEST_FACING_PLANE, SOUTH_FACING_PLANE, EAST_FACING_PLANE
from board import BoardObjective, PathObjective, Point, Segment, InvalidFillingException, InvalidFillingError
from tiling import Tiling, Tile

DEFAULT_TILE_1 = Tile([[COVERED, NORTH_FACING_PLANE]])  # orange
DEFAULT_TILE_2 = Tile([COVERED, NORTH_FACING_PLANE])  # red
DEFAULT_TILE_3 = Tile([[NORTH_FACING_PLANE, COVERED], [COVERED, UNCOVERED]])  # dark blue
DEFAULT_TILE_4 = Tile([[UNCOVERED, COVERED], [COVERED, NORTH_FACING_PLANE]])  # red
DEFAULT_TILE_5 = Tile([[COVERED, COVERED], [UNCOVERED, NORTH_FACING_PLANE]])  # light blue
DEFAULT_TILE_6 = Tile([[UNCOVERED, COVERED], [COVERED, NORTH_FACING_PLANE]])  # green

DEFAULT_TILES = [DEFAULT_TILE_1, DEFAULT_TILE_2, DEFAULT_TILE_3, DEFAULT_TILE_4, DEFAULT_TILE_4, DEFAULT_TILE_5, DEFAULT_TILE_6]

DEFAULT_LEVEL = Level(BoardObjective([], shape=(4, 4)))


class TestLevelMethods(unittest.TestCase):


    def test_invalid_tiles(self):
        level = Level(objective=BoardObjective([PathObjective(Point((0, 0)),
                                                              [Segment(SOUTH, 1)]
                                                              )], shape=(4, 4)),
                      tiles=DEFAULT_TILES)
        pass
    def test_level_5(self):
        level = Level(objective=BoardObjective([PathObjective(Point((0, 0)), [Segment(SOUTH, 1)], mandatory_planes=(0,)),
                                                PathObjective(Point((0, 3)), [Segment(WEST, 1)], mandatory_planes=(0,)),
                                                PathObjective(Point((2, 3)), [Segment(WEST, 1)], mandatory_planes=(0,)),
                                                PathObjective(Point((2, 1)), [Segment(WEST, 1)], mandatory_planes=(0,)),
                                                PathObjective(Point((1, 2)), [Segment(NORTH, 1)], mandatory_planes=(0,)),
                                                PathObjective(Point((3, 2)), [Segment(SOUTH, 1)], mandatory_planes=(0,))],
                                               shape=(4, 4)),
                      tiles=DEFAULT_TILES)

        correct_tiling = Tiling([(0,0), (0,1), (0,2), (2,0), (2,1), (2,3)],
                                [DEFAULT_TILE_1.rotation(2), DEFAULT_TILE_6, DEFAULT_TILE_4.rotation(1),
                                 DEFAULT_TILE_5.rotation(1), DEFAULT_TILE_3.rotation(2), DEFAULT_TILE_2.rotation(1)], shape=(4,4))

        self.assertIsNone(level.raise_exception_if_tiling_invalid(correct_tiling))

        wrong_tiling = Tiling([(0,0), (0,1), (0,2), (2,0), (2,1), (2,2)],
                                [DEFAULT_TILE_1.rotation(2), DEFAULT_TILE_6, DEFAULT_TILE_4.rotation(1),
                                 DEFAULT_TILE_2.rotation(1), DEFAULT_TILE_3.rotation(2), DEFAULT_TILE_5.rotation(1)], shape=(4,4))

        with self.assertRaises(InvalidFillingException):
            level.raise_exception_if_tiling_invalid(correct_tiling)

        wrong_tiles_tiling = Tiling([(0,0), (1,1), (0,2), (2,0), (2,1), (2,3)],
                                [DEFAULT_TILE_4.rotation(2), DEFAULT_TILE_2, DEFAULT_TILE_4.rotation(1),
                                 DEFAULT_TILE_5.rotation(1), DEFAULT_TILE_3.rotation(2), DEFAULT_TILE_2.rotation(1)], shape=(4,4))

        with self.assertRaises(InvalidFillingError):
            level.raise_exception_if_tiling_invalid(wrong_tiles_tiling)

if __name__ == '__main__':
    unittest.main()
