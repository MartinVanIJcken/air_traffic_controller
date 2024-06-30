import unittest

from cardinalDirections import CardinalDirection, NORTH, SOUTH, WEST, EAST


class TestCardinalDirections(unittest.TestCase):
    def test_invalid_direction(self):
        with self.assertRaises(ValueError):
            CardinalDirection("NORTHWEST")

if __name__ == '__main__':
    unittest.main()
