import unittest

from defaultLevels import level7, DEFAULT_TILE_1, DEFAULT_TILE_2, \
    DEFAULT_TILE_3, DEFAULT_TILE_4, DEFAULT_TILE_5, DEFAULT_TILE_6
from tiling import Tiling
from errorsAndExceptions import *

class TestLevelMethods(unittest.TestCase):
    def test_level_7_correct(self):
        level = level7
        correct_tiling = Tiling([(0, 0), (0, 1), (0, 2), (2, 0), (2, 1), (2, 3)],
                                [DEFAULT_TILE_1.rotation(2), DEFAULT_TILE_6, DEFAULT_TILE_4.rotation(1),
                                 DEFAULT_TILE_5.rotation(1), DEFAULT_TILE_3.rotation(2), DEFAULT_TILE_2.rotation(1)], shape=(4,4))

        self.assertIsNone(level.raise_exception_if_tiling_invalid(correct_tiling))


    def test_level_7_wrong_tiling(self):
        level = level7
        wrong_tiling = Tiling([(0, 0), (0, 1), (0, 3), (2, 0), (2, 1), (2, 2)],
                              [DEFAULT_TILE_5.rotation(1), DEFAULT_TILE_3.rotation(2), DEFAULT_TILE_2.rotation(1),
                               DEFAULT_TILE_1.rotation(2), DEFAULT_TILE_6, DEFAULT_TILE_4.rotation(1)],
                              shape=(4, 4))

        with self.assertRaises(InvalidFillingException):
            level.raise_exception_if_tiling_invalid(wrong_tiling)

    def test_level_7_wrong_tiles(self):
        level = level7
        wrong_tiles_tiling = Tiling([(0,0), (1,1), (0,2), (2,0), (2,1), (2,3)],
                                [DEFAULT_TILE_4.rotation(2), DEFAULT_TILE_2, DEFAULT_TILE_4.rotation(1),
                                 DEFAULT_TILE_5.rotation(1), DEFAULT_TILE_3.rotation(2), DEFAULT_TILE_2.rotation(1)], shape=(4,4))

        with self.assertRaises(InvalidFillingError):
            level.raise_exception_if_tiling_invalid(wrong_tiles_tiling)


if __name__ == '__main__':
    unittest.main()
