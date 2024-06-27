import unittest

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

if __name__ == '__main__':
    unittest.main()
