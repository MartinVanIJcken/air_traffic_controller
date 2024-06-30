from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
import unittest
import itertools
import numpy as np

from cardinalDirections import *
from tileComponents import Plane
from errorsAndExceptions import MissingPlaneException, PlaneLocationException, PlaneDirectionException, \
    FillingShapeError

@dataclass(frozen=True)
class Point:
    coordinates: tuple[int, int]
    def __add__(self, other):
        return Point((self[0] + other[0], self[1]+other[1]))

    def __getitem__(self, item):
        return self.coordinates[item]


class Segment:
    def __init__(self, direction: CardinalDirection, length: int):
        self.direction = direction
        self.length = length

    def locations(self, starting_location: Point) -> list[Point]:
        if self.direction is NORTH:
            return [Point(coordinates) for coordinates in
                    zip(range(starting_location[0], starting_location[0] - self.length, -1),
                        itertools.repeat(starting_location[1], self.length))]
        elif self.direction is WEST:
            return [Point(coordinates) for coordinates in
                    zip(itertools.repeat(starting_location[0], self.length),
                        range(starting_location[1], starting_location[1] + self.length))]
        elif self.direction is SOUTH:
            return [Point(coordinates) for coordinates in
                    zip(range(starting_location[0], starting_location[0] + self.length),
                        itertools.repeat(starting_location[1], self.length))]
        elif self.direction is EAST:
            return [Point(coordinates) for coordinates in
                    zip(itertools.repeat(starting_location[0], self.length),
                        range(starting_location[1], starting_location[1] - self.length, -1))]

    def displacement(self) -> np.ndarray[int]:
        if self.direction is NORTH:
            return np.array((-self.length, 0))
        elif self.direction is WEST:
            return np.array((0, self.length))
        elif self.direction is SOUTH:
            return np.array((self.length, 0))
        elif self.direction is EAST:
            return np.array((0, -self.length))

    @classmethod
    def from_points(cls, point1: Point, point2: Point):
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

    def __len__(self):
        return len(self.filling)


class Path:
    def __init__(self, start: Point, segments: list[Segment]):
        """
        Creates a path that goes from point to point in straight vertical or horizontal segments.
        """
        self.corners: list[Point] = []
        self.directions: list[CardinalDirection] = []
        self.locations: list[Point] = []
        self.segments = segments
        current_location = start
        for segment in segments:
            self.directions += [segment.direction] * segment.length
            self.locations += segment.locations(current_location)
            current_location += segment.displacement()
            self.corners.append(current_location)

        self.corners.pop()
        self.directions.append(self.directions[-1])
        self.locations.append(current_location)

    @classmethod
    def from_points(cls, points: list[Point]):
        start = points[0]
        segments = []
        for i in range(len(points) - 1):
            segments.append(Segment.from_points(points[i], points[i + 1]))

        return cls(start, segments)

    def __len__(self):
        return len(self.locations)

    def __eq__(self, other):
        return set(self.locations) == set(other.locations)

class PathObjective(Path):
    FORWARD = "FORWARD"
    BACKWARD = "BACKWARD"
    OUT = "OUT"

    def __init__(self, start: Point, segments: list[Segment], flying_forward_mandatory: bool=False,
                 mandatory_planes: tuple[int, ...]=()):
        """
        Creates that goes from point to point in straight vertical or horizontal lines
        """
        super().__init__(start, segments)

        self.flying_forward_mandatory = flying_forward_mandatory
        self.mandatory_planes = mandatory_planes

    @classmethod
    def from_points(cls, points: list[Point], flying_forward_mandatory: bool = False,
                    mandatory_planes: tuple[int, ...] = ()):
        path = Path.from_points(points)
        return cls(path.locations[0], path.segments, flying_forward_mandatory, mandatory_planes)

    @classmethod
    def from_grid(cls, grid: np.ndarray[str], start: Point, flying_forward_mandatory: bool = False,
                    mandatory_planes: tuple[int, ...] = ()):
        current_location = start
        previous_direction = 'undirected'
        points = []
        unit_steps = {'>': (0, 1), 'v': (1, 0), '^': (-1, 0), '<': (0, -1),
                      'e': (0, 1), 's': (1, 0), 'n': (-1, 0), 'w': (0, -1)}
        while True:
            current_direction = grid[current_location.coordinates]

            if current_direction != previous_direction:
                points.append(current_location)

            if current_direction == 'f':
                break

            current_location += unit_steps[current_direction]

        return PathObjective.from_points(points, flying_forward_mandatory, mandatory_planes)

    def raise_exception_if_filling_invalid(self, filling: PathFilling):
        self._check_filling_shape(filling)
        self._check_all_mandatory_planes_present(filling)
        self._check_no_planes_on_corners(filling)
        self._check_all_planes_along_path(filling)

        if self.flying_forward_mandatory:
            self._check_planes_fly_in_forward_direction(filling)
        else:
            self._check_planes_fly_in_same_direction(filling)

    def _check_filling_shape(self, filling):
        if len(filling) != len(self):
            raise FillingShapeError(f"The filling does not have the right length. Filling length is {len(filling)}, should be {len(self.locations)}.")

    def _check_all_mandatory_planes_present(self, filling: PathFilling):
        for mandatory_plane in self.mandatory_planes:
            self._check_mandatory_plane_present(filling, mandatory_plane)

    @staticmethod
    def _check_mandatory_plane_present(filling: PathFilling, mandatory_plane: int):
        if not isinstance(filling[mandatory_plane], Plane):
            raise MissingPlaneException(f"Plane missing at index {mandatory_plane}")

    def _check_no_planes_on_corners(self, filling: PathFilling):
        for corner in self.corners:
            self._check_no_plane_on_corner(corner, filling)

    def _check_no_plane_on_corner(self, corner: Point, filling: PathFilling):
        index = self.locations.index(corner)
        if isinstance(filling[index], Plane):
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
        if self.directions[location] is direction:
            return self.FORWARD
        elif self.directions[location] is direction.opposite_direction():
            return self.BACKWARD
        else:
            return self.OUT

    def __eq__(self, other):
        return super().__eq__(other) \
               and self.mandatory_planes == other.mandatory_planes \
                and self.flying_forward_mandatory == other.flying_forward_mandatory \
                and (self.locations[0] == other.locations[0] or not self.flying_forward_mandatory)

@dataclass
class BoardFilling:
    def __init__(self, filling: Iterable[Iterable[...]]):
        self.filling = np.array(filling)

        self.shape = self.filling.shape

        if len(self.filling.shape) != 2:
            raise ValueError("Filling is not a rectangle.")

    def __getitem__(self, item: Point):
        if not isinstance(item, Point):
            raise ValueError(item)
        return self.filling[item.coordinates]

    def restrict_to_path(self, path: Path):
        return PathFilling([self[location] for location in path.locations])

    def enumerate_just_the_planes(self):
        for i, row in enumerate(self.filling):
            for j, content in enumerate(row):
                if isinstance(content, Plane):
                    yield Point((i, j)), content


class BoardObjective:
    def __init__(self, paths: list[PathObjective, ...], shape: tuple[int, int]):
        self.shape = shape
        self.paths = paths

        self._raise_error_if_paths_outside_board()
        self.allowed_plane_locations = set([location for path in paths for location in path.locations])


    def _raise_error_if_paths_outside_board(self):
        for path in self.paths:
            for location in itertools.chain([path.locations[0], path.locations[-1]], path.corners):
                if location[0] < 0 or location[1] < 0 or location[0] >= self.shape[0] or location[1] >= self.shape[1]:
                    raise ValueError("Paths do not fit within width of board.")

    @classmethod
    def from_string(cls, board_objective_str: str):
        """
        Create a board objective from a string. Does not support overlapping path.
        A path starts with w, s, n, e for the direction to go into and then is continued using
        >, v, ^, < to indicate continuation of the same path, ending with an f
        :param board_objective_str:
        :return:
        """
        paths = []
        board_objective_arr = np.array([list(row) for row in board_objective_str.split('\n')])
        for loc, char in np.ndenumerate(board_objective_arr):
            if char in ('n', 'w', 's', 'e'):
                paths.append(PathObjective.from_grid(board_objective_arr, Point(loc)))
        return cls(paths, shape=board_objective_arr.shape)
    @staticmethod
    def _create_path_objective_from_arr(board_objective_arr, start: Point) -> PathObjective:
        current_location = start
        previous_direction = 'undirected'
        points = []
        unit_steps = {'>': (0,1), 'v': (1,0), '^': (-1,0), '<': (0,-1),
                      'e': (0, 1), 's': (1, 0), 'n': (-1, 0), 'w': (0, -1)}
        while True:
            current_direction = board_objective_arr[current_location]

            if current_direction != previous_direction:
                points.append(current_location)

            if current_direction == 'f':
                break

            current_location += unit_steps[current_direction]

        return PathObjective.from_points(points)


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
            if location not in self.allowed_plane_locations:
                raise PlaneLocationException(f"Plane at {location} is outside the allowed paths.")

    def __eq__(self, other):
        for path in self.paths:
            if path not in other.paths:
                return False

        for path in other.paths:
            if path not in self.paths:
                return False

        return self.shape == other.shape

