from __future__ import annotations

from abc import abstractmethod, ABC
import numpy as np

from cardinalDirections import *

class TileComponent(ABC):
    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def rotate(self, k):
        pass


class Plane(TileComponent):
    ORDERED_PLANES_COUNTERCLOCKWISE: tuple[Plane, Plane, Plane, Plane]
    def __init__(self, direction: CardinalDirection, symbol: str):
        self.direction = direction

    def __repr__(self):
        return {NORTH: '^', WEST: '>', SOUTH: 'v', EAST: '>'}[self.direction]

    def rotate(self, k):
        i = self.ORDERED_PLANES_COUNTERCLOCKWISE.index(self)
        return self.ORDERED_PLANES_COUNTERCLOCKWISE[(i+k)%4]

class RotationInvariantComponent(TileComponent):
    def __init__(self, symbol:str):
        self.symbol = symbol

    def __repr__(self):
        return self.symbol

    def rotate(self, k):
        return self

NORTH_FACING_PLANE = Plane(NORTH, '^')
WEST_FACING_PLANE = Plane(WEST, '>')
SOUTH_FACING_PLANE = Plane(SOUTH, 'v')
EAST_FACING_PLANE = Plane(EAST, '<')

Plane.ORDERED_PLANES_COUNTERCLOCKWISE = [NORTH_FACING_PLANE, WEST_FACING_PLANE, SOUTH_FACING_PLANE, EAST_FACING_PLANE]
COVERED = RotationInvariantComponent('o')
UNCOVERED = RotationInvariantComponent(' ')

class Tile:
    def __init__(self, content: np.ndarray[TileComponent]):
        self.content = np.array(content)

    def rotation(self, k: int):
        """
        Rotate the tile by a multiple of 90 degrees.
        :param k: The number of times the tile is rotated by 90 degrees
        :return: A tile with the same contents but rotated by k*90 degrees counterclockwise
        """
        new_content = self.rotate_components(np.rot90(self.content, k), k)
        return Tile(new_content)
    @staticmethod
    def rotate_components(content, k):
        new_content = []
        for row in content:
            new_content.append([])
            for tile in row:
                if isinstance(tile, Plane):
                    new_content[-1].append(tile.rotate(k))
                else:
                    new_content[-1].append(tile)

        return new_content

    def __eq__(self, other):
        return np.array_equal(self.content, other.content)

    def __repr__(self):
        return repr(self.content)

tile = Tile([[WEST_FACING_PLANE, COVERED],
                 [UNCOVERED, COVERED],
                 [UNCOVERED, COVERED]])
print(tile.rotation(1))
