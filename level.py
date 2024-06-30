from board import BoardObjective
from tiling import Tile
from collections import Counter


class Level:
    def __init__(self, objective: BoardObjective, tiles: list[Tile]):
        self.objective = objective
        self.tiles = tiles

    def raise_exception_if_tiling_invalid(self, tiling):
        if Counter(self.tiles) != Counter(tiling.tiles):
            raise ValueError("These are not the right tiles")