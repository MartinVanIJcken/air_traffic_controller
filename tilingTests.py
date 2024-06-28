import unittest

from tileComponents import NORTH_FACING_PLANE, WEST_FACING_PLANE, SOUTH_FACING_PLANE, EAST_FACING_PLANE, COVERED, UNCOVERED
from tiling import *

class TestTileMethods(unittest.TestCase):
    def test_rotate(self):
        tile = Tile([[WEST_FACING_PLANE, COVERED],
                     [UNCOVERED, COVERED],
                     [UNCOVERED, COVERED]])

        rotated_tile_1 = Tile([[COVERED, COVERED, COVERED],
                     [SOUTH_FACING_PLANE, UNCOVERED, UNCOVERED]])
        rotated_tile_2 = Tile([[COVERED, UNCOVERED],
                               [COVERED, UNCOVERED],
                               [COVERED, EAST_FACING_PLANE]])
        rotated_tile_3 = Tile([[UNCOVERED, UNCOVERED, NORTH_FACING_PLANE],
                               [COVERED, COVERED, COVERED]])

        self.assertEqual(tile.rotation(0), tile)
        self.assertEqual(tile.rotation(1), rotated_tile_1)
        self.assertEqual(tile.rotation(2), rotated_tile_2)
        self.assertEqual(tile.rotation(3), rotated_tile_3)
        self.assertEqual(tile.rotation(4), tile)

    def test_enumerate(self):
        tile = Tile([[NORTH_FACING_PLANE, COVERED],
              [COVERED, COVERED],
              [UNCOVERED, COVERED]])
        self.assertEqual(set(tile.enumerate_components()),
                         {((0, 0), NORTH_FACING_PLANE), ((0, 1), COVERED), ((1, 0), COVERED),
                          ((1, 1), COVERED), ((2, 0), UNCOVERED), ((2, 1), COVERED)})
class TestTilingMethods(unittest.TestCase):
    DEFAULT_TILE_1 = Tile([[COVERED, UNCOVERED],
                               [COVERED, UNCOVERED],
                               [COVERED, EAST_FACING_PLANE]])
    DEFAULT_TILE_2 = Tile([[NORTH_FACING_PLANE, COVERED],
              [COVERED, COVERED],
              [UNCOVERED, COVERED]])
    def test_filling(self):
        tiling = Tiling([(0, 0), (0, 1)], [self.DEFAULT_TILE_1, self.DEFAULT_TILE_2], shape=(4, 4))
        self.assertEqual(tiling.filling,
                         BoardFilling([[COVERED, NORTH_FACING_PLANE, COVERED, UNCOVERED],
                                       [COVERED, COVERED, COVERED, COVERED],
                                       [COVERED, EAST_FACING_PLANE, COVERED, UNCOVERED],
                                       [UNCOVERED, UNCOVERED, UNCOVERED, UNCOVERED]]))

    def test_overlapping_tiles_at_creation(self):
        with self.assertRaises(ValueError):
            Tiling([(0, 0), (0, 0)], [self.DEFAULT_TILE_1, self.DEFAULT_TILE_2], shape=(4, 4))

    def test_overlapping_tiles_at_addition(self):
        tiling = Tiling([(0, 0)], [self.DEFAULT_TILE_1], shape=(4, 4))
        with self.assertRaises(ValueError):
            tiling.add_tile((0, 0), self.DEFAULT_TILE_2)

    def test_tile_outside_grid(self):
        with self.assertRaises(ValueError):
            Tiling([(0, 3)], [self.DEFAULT_TILE_1], shape=(4, 4))


if __name__ == '__main__':
    unittest.main()
