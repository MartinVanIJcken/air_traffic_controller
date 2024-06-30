import itertools

from tiling import Tile
from tileComponents import *
from level import Level
from board import BoardObjective, PathObjective, Segment

DEFAULT_TILE_1 = Tile([[COVERED], [NORTH_FACING_PLANE]])  # orange
DEFAULT_TILE_2 = Tile([[COVERED, NORTH_FACING_PLANE]])  # red
DEFAULT_TILE_3 = Tile([[NORTH_FACING_PLANE, COVERED], [COVERED, UNCOVERED]])  # dark blue
DEFAULT_TILE_4 = Tile([[UNCOVERED, COVERED], [COVERED, NORTH_FACING_PLANE]])  # red
DEFAULT_TILE_5 = Tile([[COVERED, COVERED], [UNCOVERED, NORTH_FACING_PLANE]])  # light blue
DEFAULT_TILE_6 = Tile([[COVERED, UNCOVERED], [COVERED, NORTH_FACING_PLANE]])  # green

DEFAULT_TILES = [DEFAULT_TILE_1, DEFAULT_TILE_2, DEFAULT_TILE_3, DEFAULT_TILE_4, DEFAULT_TILE_5, DEFAULT_TILE_6]

# a hack to get a shorthand for all points
for i, j in itertools.product(range(4), range(4)):
    globals()["p"+i+j] = Point((i,j))

level7 = Level(objective=BoardObjective([PathObjective(p00, [Segment(SOUTH, 1)], mandatory_planes=(0,)),
                                         PathObjective(p03, [Segment(WEST, 1)], mandatory_planes=(0,)),
                                         PathObjective(p23, [Segment(WEST, 1)], mandatory_planes=(0,)),
                                         PathObjective(p21, [Segment(WEST, 1)], mandatory_planes=(0,)),
                                         PathObjective(p12, [Segment(NORTH, 1)], mandatory_planes=(0,)),
                                         PathObjective(p32, [Segment(SOUTH, 1)], mandatory_planes=(0,))],
                                        shape=(4, 4)),
               tiles=DEFAULT_TILES)

# TODO levels 8 through 47

level48 = Level(objective=BoardObjective([PathObjective(p00, [Segment(SOUTH, 4)]),
                                          PathObjective(p01, [Segment(SOUTH, 4)]),
                                          PathObjective(p33, [Segment(WEST, 0), Segment(NORTH, 3),
                                                              Segment(WEST, 1), Segment(SOUTH, 4)])],
                                         shape=(4, 4)),
                tiles=DEFAULT_TILES)
