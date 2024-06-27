from dataclasses import dataclass

from cardinalDirections import *
class TileComponent:
    pass

@dataclass
class Plane(TileComponent):
    direction: CardinalDirection


NORTH_FACING_PLANE = Plane(NORTH)
WEST_FACING_PLANE = Plane(WEST)
SOUTH_FACING_PLANE = Plane(SOUTH)
EAST_FACING_PLANE = Plane(EAST)

EMPTY = TileComponent()

class Tile:
    pass