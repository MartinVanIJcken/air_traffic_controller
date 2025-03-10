from __future__ import annotations

import numpy as np

from tileComponents import TileComponent, UNCOVERED
from board import BoardFilling
from errorsAndExceptions import TileLocationError

TileContentType = list[list[TileComponent]]

class Tile:
    def __init__(self, content: TileContentType):
        self.content = np.array(content)
        self.has_been_rotated_by = 0

    def rotation(self, k: int):
        """
        Rotate the tile by a multiple of 90 degrees.
        :param k: The number of times the tile is rotated by 90 degrees
        :return: A tile with the same contents but rotated by k*90 degrees counterclockwise
        """
        new_content = self.rotate_components(np.rot90(self.content, k), k)
        new_tile = Tile(new_content)
        new_tile.has_been_rotated_by = (self.has_been_rotated_by+k)%4
        return new_tile

    @staticmethod
    def rotate_components(content, k) -> TileContentType:
        new_content = []
        for row in content:
            new_content.append([])
            for tile in row:
                new_content[-1].append(tile.rotate(k))

        return new_content

    def __eq__(self, other: Tile):
        return np.array_equal(self.rotation(-self.has_been_rotated_by+other.has_been_rotated_by).content, other.content)

    def __repr__(self):
        return repr(self.content)

    def __hash__(self):
        unrotated_tile = self.rotation(-self.has_been_rotated_by)
        return hash(unrotated_tile.content.tostring())

    def enumerate_components(self):
        return np.ndenumerate(self.content)

class Tiling:
    def __init__(self, top_left_corners: list[tuple[int, int]], tiles: list[Tile], shape: tuple[int, int]):
        self.tiles = tiles
        self._filling = np.full(shape, UNCOVERED)

        for top_left_corner, tile in zip(top_left_corners, tiles):
            self.add_tile(top_left_corner, tile)

    @property
    def filling(self) -> BoardFilling:
        return BoardFilling(self._filling)

    def add_tile(self, top_left_corner: tuple[int, int], tile: Tile):
        for relative_location, component in tile.enumerate_components():
            if component is UNCOVERED:
                continue
            absolute_location = tuple(top_left_corner + np.array(relative_location))
            try:
                if self._filling[absolute_location] is not UNCOVERED:
                    raise TileLocationError(f"The tiles overlap at location {absolute_location}.")
            except IndexError:
                raise TileLocationError("Tile lies outside the board.")
            self._filling[absolute_location] = component
