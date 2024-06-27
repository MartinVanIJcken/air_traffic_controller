from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
import unittest
import itertools
import numpy as np

class InvalidFillingError(Exception):
    pass


class FillingShapeError(InvalidFillingError):
    pass

class InvalidFillingException(Exception):
    pass


class MissingPlaneException(InvalidFillingException):
    pass


class PlaneDirectionException(InvalidFillingException):
    pass


class PlaneLocationException(InvalidFillingException):
    pass


class CardinalDirection:
    __match_args__ = tuple("direction")

    def __init__(self, direction):
        if direction not in "NORTH SOUTH WEST EAST".split():
            raise ValueError(f"{direction} is not a cardinal direction.")
        self.direction = direction

    def opposite_direction(self):
        if self.direction == "NORTH":
            return CardinalDirection("SOUTH")
        elif self.direction == "WEST":
            return CardinalDirection("EAST")
        elif self.direction == "SOUTH":
            return CardinalDirection("NORTH")
        elif self.direction == "EAST":
            return CardinalDirection("WEST")

    def __eq__(self, other):
        return self.direction == other.direction

    def __repr__(self):
        return self.direction


NORTH = CardinalDirection("NORTH")
WEST = CardinalDirection("WEST")
SOUTH = CardinalDirection("SOUTH")
EAST = CardinalDirection("EAST")
EMPTY = "Empty"


@dataclass
class Plane:
    direction: CardinalDirection


NORTH_FACING_PLANE = Plane(NORTH)
WEST_FACING_PLANE = Plane(WEST)
SOUTH_FACING_PLANE = Plane(SOUTH)
EAST_FACING_PLANE = Plane(EAST)


class Segment:
    def __init__(self, direction: CardinalDirection, length: int):
        self.direction = direction
        self.length = length

    def locations(self, starting_location) -> list[tuple[int, int]]:
        match self.direction:
            case CardinalDirection(direction="NORTH"):
                return list(zip(range(starting_location[0], starting_location[0] - self.length, -1),
                                itertools.repeat(starting_location[1], self.length)))
            case CardinalDirection(direction="WEST"):
                return list(zip(itertools.repeat(starting_location[0], self.length),
                                range(starting_location[1], starting_location[1] + self.length)))
            case CardinalDirection(direction="SOUTH"):
                return list(zip(range(starting_location[0], starting_location[0] + self.length),
                                itertools.repeat(starting_location[1], self.length)))
            case CardinalDirection(direction="EAST"):
                return list(zip(itertools.repeat(starting_location[0], self.length),
                                range(starting_location[1], starting_location[1] - self.length, -1)))

    def displacement(self) -> np.ndarray[int]:
        match self.direction:
            case CardinalDirection(direction="NORTH"):
                return np.array((-self.length, 0))
            case CardinalDirection(direction="WEST"):
                return np.array((0, self.length))
            case CardinalDirection(direction="SOUTH"):
                return np.array((self.length, 0))
            case CardinalDirection(direction="EAST"):
                return np.array((0, -self.length))

    @classmethod
    def from_points(cls, point1, point2):
        if point1[0] != point2[0] and point1[1] != point2[1]:
            raise ValueError("Given points do not lie along a cardinal direction.")
        if point1[0] < point2[0]:
            return Segment(SOUTH, point2[0] - point1[0])
        elif point1[1] < point2[1]:
            return Segment(WEST, point2[1] - point1[1])
        elif point1[1] > point2[1]:
            return Segment(EAST, point1[1] - point2[1])
        elif point1[0] > point2[0]:
            return Segment(NORTH, point1[0] - point2[0])
        else:  # point1 == point2:
            raise ValueError("Given points create a segment of length 0. It is not possible to infer the direction.")


@dataclass
class PathFilling:
    filling: list

    def enumerate_just_the_planes(self):
        for i, content in enumerate(self.filling):
            if isinstance(content, Plane):
                yield i, content

    def __getitem__(self, item):
        return self.filling[item]


Point = np.array


class Path:
    def __init__(self, start: Point, segments: list[Segment]):
        """
        Creates that goes from point to point in straight vertical or horizontal segments
        """
        self.corners = []
        self.directions = []
        self.locations = []
        self.segments = segments
        current_location = start
        for segment in segments:
            self.directions += [segment.direction] * segment.length
            self.locations += segment.locations(current_location)
            current_location += segment.displacement()
            self.corners.append(tuple(current_location))

        self.corners.pop()
        self.directions.append(self.directions[-1])
        self.locations.append(tuple(current_location))

    @classmethod
    def from_points(cls, points: tuple[tuple[int, int], ...]):
        points = list(map(np.array, points))
        start = points[0]
        segments = []
        for i in range(len(points) - 1):
            segments.append(Segment.from_points(points[i], points[i + 1]))
        return cls(start, segments)


class PathObjective(Path):
    FORWARD = "FORWARD"
    BACKWARD = "BACKWARD"
    OUT = "OUT"

    def __init__(self, start: Point, segments: list[Segment], flying_forward_mandatory: bool,
                 mandatory_planes: tuple[int]):
        """
        Creates that goes from point to point in straight vertical or horizontal lines
        """
        super().__init__(start, segments)

        self.flying_forward_mandatory = flying_forward_mandatory
        self.mandatory_planes = mandatory_planes

    @classmethod
    def from_points(cls, points: tuple[tuple[int, int], ...], flying_forward_mandatory: bool = False,
                    mandatory_planes: tuple[int, ...] = ()):
        path = Path.from_points(points)
        return cls(path.locations[0], path.segments, flying_forward_mandatory, mandatory_planes)

    def raise_exception_if_filling_invalid(self, filling: PathFilling):
        self._check_all_mandatory_planes_present(filling)
        self._check_no_planes_on_corners(filling)
        self._check_all_planes_along_path(filling)

        if self.flying_forward_mandatory:
            self._check_planes_fly_in_forward_direction(filling)
        else:
            self._check_planes_fly_in_same_direction(filling)

    def _check_all_mandatory_planes_present(self, filling: PathFilling):
        for mandatory_plane in self.mandatory_planes:
            self._check_mandatory_plane_present(filling, mandatory_plane)

    @staticmethod
    def _check_mandatory_plane_present(filling, mandatory_plane):
        if filling[mandatory_plane] == EMPTY:
            raise MissingPlaneException(f"Plane missing at index {mandatory_plane}")

    def _check_no_planes_on_corners(self, filling: PathFilling):
        for corner in self.corners:
            self._check_no_plane_on_corner(corner, filling)

    def _check_no_plane_on_corner(self, corner, filling):
        index = self.locations.index(corner)
        if filling[index] != EMPTY:
            raise PlaneLocationException

    def _check_all_planes_along_path(self, filling: PathFilling):
        for i, plane in filling.enumerate_just_the_planes():
            if self._forward_backward_or_out(i, plane.direction) == self.OUT:
                raise PlaneDirectionException(f"Plane at index {i} not along path")

    def _check_planes_fly_in_forward_direction(self, filling: PathFilling):
        for i, plane in filling.enumerate_just_the_planes():
            if self._forward_backward_or_out(i, plane.direction) != self.FORWARD:
                raise PlaneDirectionException(f"Plane at index {i} not flying forward")

    def _check_planes_fly_in_same_direction(self, filling: PathFilling):
        previous_direction = None

        for i, plane in filling.enumerate_just_the_planes():

            if previous_direction is None:
                previous_direction = self._forward_backward_or_out(i, plane.direction)
                prev_i = i
                continue

            current_direction = self._forward_backward_or_out(i, plane.direction)
            if previous_direction != current_direction:
                raise PlaneDirectionException(f"Planes at indices {prev_i} and {i} are going in different directions.")

            prev_i = i
            previous_direction = current_direction

    def _forward_backward_or_out(self, location, direction):
        if self.directions[location] == direction:
            return self.FORWARD
        elif self.directions[location] == direction.opposite_direction():
            return self.BACKWARD
        else:
            return self.OUT

@dataclass
class BoardFilling:
    def __init__(self, filling: Iterable[Iterable[...]]):
        self.filling = np.array(filling)

        self.shape = self.filling.shape

        if len(self.filling.shape) != 2:
            raise ValueError("Filling is not a rectangle.")

    def __getitem__(self, item):
        return self.filling[item]

    def restrict_to_path(self, path: Path):
        return PathFilling([self[location] for location in path.locations])

    def enumerate_just_the_planes(self):
        for i, row in enumerate(self.filling):
            for j, content in enumerate(row):
                if isinstance(content, Plane):
                    yield (i, j), content


class BoardObjective:
    def __init__(self, paths: tuple[PathObjective, ...], shape: tuple[int, int]):
        self.shape = shape
        self.paths = paths

        self._raise_error_if_paths_outside_board()
        self.allowed_plane_locations = set([location for path in paths for location in path.locations])

    def _raise_error_if_paths_outside_board(self):
        for path in self.paths:
            for location in itertools.chain([path.locations[0], path.locations[-1]], path.corners):
                if location[0] < 0 or location[1] < 0 or location[0] >= self.shape[0] or location[1] >= self.shape[1]:
                    raise ValueError("Paths do not fit within width of board.")

    def raise_exception_if_filling_invalid(self, board_filling: BoardFilling):
        self._check_filling_dimensions(board_filling)
        self._check_all_planes_on_path(board_filling)

        for path in self.paths:
            path_filling = board_filling.restrict_to_path(path)
            path.raise_exception_if_filling_invalid(path_filling)

    def _check_filling_dimensions(self, board_filling):
        if board_filling.shape != self.shape:
            raise FillingShapeError("Filling does not have the same shape as the board.")

    def _check_all_planes_on_path(self, filling: BoardFilling):
        for location, plane in filling.enumerate_just_the_planes():
            print(location, plane)
            if location not in self.allowed_plane_locations:
                raise PlaneLocationException(f"Plane at {location} is outside the allowed paths.")


if __name__ == '__main__':
    unittest.main()
