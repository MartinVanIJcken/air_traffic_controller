from __future__ import annotations

from abc import abstractmethod, ABC

from cardinalDirections import *

class TileComponent(ABC):
    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def rotate(self, k):
        pass


class Plane(TileComponent):
    _PLANES_ORDERED_COUNTERCLOCKWISE: tuple[Plane, Plane, Plane, Plane]
    def __init__(self, direction: CardinalDirection, symbol: str):
        self.direction = direction

    def __repr__(self):
        return {NORTH: '^', WEST: '>', SOUTH: 'v', EAST: '>'}[self.direction]

    def rotate(self, k):
        i = self._PLANES_ORDERED_COUNTERCLOCKWISE.index(self)
        return self._PLANES_ORDERED_COUNTERCLOCKWISE[(i + k) % 4]

class RotationInvariantTileComponent(TileComponent):
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

Plane._PLANES_ORDERED_COUNTERCLOCKWISE = [NORTH_FACING_PLANE, WEST_FACING_PLANE, SOUTH_FACING_PLANE, EAST_FACING_PLANE]
COVERED = RotationInvariantTileComponent('o')
UNCOVERED = RotationInvariantTileComponent(' ')
