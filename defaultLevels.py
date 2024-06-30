import itertools

from tiling import Tile
from tileComponents import *
from level import Level
from board import BoardObjective, PathObjective, Segment, Point

DEFAULT_TILE_1 = Tile([[COVERED], [NORTH_FACING_PLANE]])  # orange
DEFAULT_TILE_2 = Tile([[COVERED, NORTH_FACING_PLANE]])  # red
DEFAULT_TILE_3 = Tile([[NORTH_FACING_PLANE, COVERED], [COVERED, UNCOVERED]])  # dark blue
DEFAULT_TILE_4 = Tile([[UNCOVERED, COVERED], [COVERED, NORTH_FACING_PLANE]])  # red
DEFAULT_TILE_5 = Tile([[COVERED, COVERED], [UNCOVERED, NORTH_FACING_PLANE]])  # light blue
DEFAULT_TILE_6 = Tile([[COVERED, UNCOVERED], [COVERED, NORTH_FACING_PLANE]])  # green

DEFAULT_TILES = [DEFAULT_TILE_1, DEFAULT_TILE_2, DEFAULT_TILE_3, DEFAULT_TILE_4, DEFAULT_TILE_5, DEFAULT_TILE_6]

p00 = Point((0, 0))
p01 = Point((0, 1))
p02 = Point((0, 2))
p03 = Point((0, 3))
p10 = Point((1, 0))
p11 = Point((1, 1))
p12 = Point((1, 2))
p13 = Point((1, 3))
p20 = Point((2, 0))
p21 = Point((2, 1))
p22 = Point((2, 2))
p23 = Point((2, 3))
p30 = Point((3, 0))
p31 = Point((3, 1))
p32 = Point((3, 2))
p33 = Point((3, 3))

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
