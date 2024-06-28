import numpy as np

from tileComponents import TileComponent
from board import BoardFilling

TileContentType = np.ndarray[TileComponent]

class Tile:
    def __init__(self, content: TileContentType):
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
    def rotate_components(content, k) -> TileContentType:
        new_content = []
        for row in content:
            new_content.append([])
            for tile in row:
                new_content[-1].append(tile.rotate(k))

        return new_content

    def __eq__(self, other):
        return np.array_equal(self.content, other.content)

    def __repr__(self):
        return repr(self.content)

class Tiling:
    def __init__(self, tiles: dict[tuple[int, int], Tile]):
        self.tiles = tiles

    def to_filling(self) -> BoardFilling:
