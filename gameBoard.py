from dataclasses import dataclass
import unittest
import itertools
import numpy as np



class TestPathMethods(unittest.TestCase):
    def test_path_from_points(self):
        path = Path.from_points([(1,1), (3,1), (3,2), (1,2)])
        self.assertEqual(path.locations, [(1, 1), (2, 1), (3, 1), (3, 2), (2, 2), (1, 2)])
        
    def test_good_path_gets_accepted(self):
        path = Path.from_points([(1,1), (3,1), (3,2), (1,2)])
        filling = Filling([EMPTY, NORTH_FACING_PLANE, EMPTY, EMPTY, SOUTH_FACING_PLANE])
        self.assertTrue(path.verify_filling(filling))

    def test_plane_not_along_path(self):
        path = Path.from_points([(1,1), (3,1), (3,2)])
        filling = Filling([EMPTY, NORTH_FACING_PLANE, EMPTY, NORTH_FACING_PLANE])
        with self.assertRaises(PlaneDirectionError):
            path.verify_filling(filling)
            
    def test_planes_in_different_directions(self):
        path = Path.from_points([(1,1), (3,1), (3,2)])
        filling = Filling([EMPTY, NORTH_FACING_PLANE, EMPTY, WEST_FACING_PLANE])
        with self.assertRaises(PlaneDirectionError):
            path.verify_filling(filling)

    def test_plane_on_corner(self):
        path = Path.from_points([(1,1), (3,1), (3,2)])
        filling = Filling([EMPTY, NORTH_FACING_PLANE, NORTH_FACING_PLANE, EMPTY])
        with self.assertRaises(PlaneLocationError):
            path.verify_filling(filling)

    def test_plane_at_start_and_end(self):
        path = Path.from_points([(1,1), (1,4), (3,4)])
        filling = Filling([WEST_FACING_PLANE, EMPTY, EMPTY, EMPTY, EMPTY, SOUTH_FACING_PLANE])
        self.assertTrue(path.verify_filling(filling))
        
    def test_bad_plane_at_end(self):
        path = Path.from_points([(1,1), (1,4), (3,4)])
        filling = Filling([EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WEST_FACING_PLANE])
        with self.assertRaises(PlaneDirectionError):
            self.assertTrue(path.verify_filling(filling))

    def test_bad_plane_at_start(self):
        path = Path.from_points([(1,1), (1,4), (3,4)])
        filling = Filling([SOUTH_FACING_PLANE, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY])
        with self.assertRaises(PlaneDirectionError):
            self.assertTrue(path.verify_filling(filling))
        
    def test_directed_path_followed(self):
        path = Path.from_points([(1,1), (1,4), (3,4)], flying_forward_mandatory=True)
        filling = Filling([WEST_FACING_PLANE, EMPTY, EMPTY, EMPTY, EMPTY, SOUTH_FACING_PLANE])
        self.assertTrue(path.verify_filling(filling))

    def test_directed_path_not_followed(self):
        path = Path.from_points([(3,4), (1,4), (1,1)], flying_forward_mandatory=True)
        filling = Filling([WEST_FACING_PLANE, EMPTY, EMPTY, EMPTY, EMPTY, SOUTH_FACING_PLANE])
        with self.assertRaises(PlaneDirectionError):
            path.verify_filling(filling)
    
    def test_mandatory_planes_present(self):
        path = Path.from_points([(50, 43), (50, 50)], mandatory_planes=[0,1,2])
        filling = Filling([WEST_FACING_PLANE, WEST_FACING_PLANE, WEST_FACING_PLANE, EMPTY, EMPTY, WEST_FACING_PLANE, EMPTY, EMPTY])
        self.assertTrue(path.verify_filling(filling))

    def test_mandatory_plane_missing(self):
        path = Path.from_points([(50, 43), (50, 50)], mandatory_planes=[0,1,2])
        filling = Filling([WEST_FACING_PLANE, EMPTY, WEST_FACING_PLANE, EMPTY, EMPTY, WEST_FACING_PLANE, EMPTY, EMPTY])
        with self.assertRaises(MissingPlaneError):
            path.verify_filling(filling)
                

class MissingPlaneError(Exception):
    pass

class PlaneDirectionError(Exception):
    pass

class PlaneLocationError(Exception):
    pass



class CompassDirection:
    __match_args__ = tuple("direction")
    def __init__(self, direction):
        self.direction = direction
    
    
    def opposite_direction(self):
        if self.direction == "NORTH":
            return CompassDirection("SOUTH")
        elif self.direction == "WEST":
            return CompassDirection("EAST")
        elif self.direction == "SOUTH":
            return CompassDirection("NORTH")
        elif self.direction == "EAST":
            return CompassDirection("WEST")

    def __eq__(self, other):
        return self.direction == other.direction

NORTH = CompassDirection("NORTH")
WEST = CompassDirection("WEST")
SOUTH = CompassDirection("SOUTH")
EAST = CompassDirection("EAST")
EMPTY = "Empty"


@dataclass
class Plane:
    direction: str


NORTH_FACING_PLANE = Plane(NORTH)
WEST_FACING_PLANE = Plane(WEST)
SOUTH_FACING_PLANE = Plane(SOUTH)
EAST_FACING_PLANE = Plane(EAST)

class Segment:
    def __init__(self, direction: str, length: int):
        self.direction = direction
        self.length = length

    def locations(self, starting_location):
        match self.direction:
            case CompassDirection(direction="NORTH"):
                return list(zip(range(starting_location[0], starting_location[0] - self.length, -1), itertools.repeat(starting_location[1], self.length)))
            case CompassDirection(direction="WEST"):
                return list(zip(itertools.repeat(starting_location[0], self.length), range(starting_location[1], starting_location[1] + self.length)))
            case CompassDirection(direction="SOUTH"):
                return list(zip(range(starting_location[0], starting_location[0] + self.length), itertools.repeat(starting_location[1], self.length)))
            case CompassDirection(direction="EAST"):
                return list(zip(itertools.repeat(starting_location[0], self.length), range(starting_location[1], starting_location[1] - self.length, -1)))

    def displacement(self):
        match self.direction:
            case CompassDirection(direction="NORTH"):
                return np.array((-self.length, 0))
            case CompassDirection(direction="WEST"):
                return np.array((0, self.length))
            case CompassDirection(direction="SOUTH"):
                return np.array((self.length, 0))
            case CompassDirection(direction="EAST"):
                return np.array((0, -self.length))

    @classmethod
    def from_points(cls, point1, point2):
        if point1[0] < point2[0]:
            return Segment(SOUTH, point2[0] - point1[0])
        elif point1[1] < point2[1]:
            return Segment(WEST, point2[1] - point1[1])
        elif point1[1] > point2[1]:
            return Segment(EAST, point1[1] - point2[1])
        elif point1[0] > point2[0]:
            return Segment(NORTH, point1[0] - point2[0])
        

@dataclass
class Filling:
    filling: list

    def enumerate_just_the_planes(self):
        for i, content in enumerate(self.filling):
            if content == EMPTY:
                continue
            yield i, content

    def __getitem__(self, index):
        return self.filling[index]
class Path:
    FORWARD = "FORWARD"
    BACKWARD = "BACKWARD"
    OUT = "OUT"
    
    def __init__(self, start: np.array, segments: list[Segment], flying_forward_mandatory: bool, mandatory_planes:list[int]):
        """
        Creates that goes from point to point in straight vertical or horizontal lines
        """
        self.corners = []
        self.directions = []
        self.locations = []
        current_location = start
        for segment in segments:
            self.directions += [segment.direction]*segment.length
            self.locations += segment.locations(current_location)
            current_location += segment.displacement()
            self.corners.append(tuple(current_location))
        
        self.corners.pop()
        self.directions.append(self.directions[-1])
        self.locations.append(tuple(current_location))
        
        self.flying_forward_mandatory = flying_forward_mandatory
        self.mandatory_planes = mandatory_planes
        
    @classmethod
    def from_points(cls, points, flying_forward_mandatory: bool=False, mandatory_planes:list[int]=[]):
        points = list(map(np.array, points))
        start = points[0]
        segments = []
        for i in range(len(points)-1):
            segments.append(Segment.from_points(points[i], points[i+1]))
        return cls(start, segments, flying_forward_mandatory, mandatory_planes)

        
    def verify_filling(self, filling: Filling):
        self._check_all_mandatory_planes_present(filling)
        self._check_no_planes_on_corners(filling)
        self._check_all_planes_along_path(filling)
        
        if self.flying_forward_mandatory:
            self._check_planes_fly_in_forward_direction(filling)
        else:
            self._check_planes_fly_in_same_direction(filling)

        return True

    def _check_all_mandatory_planes_present(self, filling: Filling):
        for mandatory_plane in self.mandatory_planes:
            self._check_mandatory_plane_present(filling, mandatory_plane)

    def _check_mandatory_plane_present(self, filling, mandatory_plane):
        if filling[mandatory_plane] == EMPTY:
            raise MissingPlaneError(f"Plane missing at location {mandatory_plane}")

    def _check_no_planes_on_corners(self, filling: Filling):
        for corner in self.corners:
            self._check_no_plane_on_corner(corner, filling)

    def _check_no_plane_on_corner(self, corner, filling):
        index = self.locations.index(corner)
        if filling[index] != EMPTY:
            raise PlaneLocationError

    def _check_all_planes_along_path(self, filling: Filling):
        for location, plane in filling.enumerate_just_the_planes():
            if self._forward_backward_or_out(location, plane.direction) == self.OUT:
                raise PlaneDirectionError(f"Plane at {location} not along path")
    
    def _check_planes_fly_in_forward_direction(self, filling: Filling):
        for location, plane in filling.enumerate_just_the_planes():
            if self._forward_backward_or_out(location, plane.direction) != self.FORWARD:
                raise PlaneDirectionError("Plane not flying forward")

    def _check_planes_fly_in_same_direction(self, filling: Filling):
        previous_direction = None
        for location, plane in filling.enumerate_just_the_planes():
        
            if previous_direction is None:
                previous_direction = self._forward_backward_or_out(location, plane.direction)
                continue

            current_direction = self._forward_backward_or_out(location, plane.direction)
            if previous_direction != current_direction:
                raise PlaneDirectionError("Not all planes are going in the same direction.")

            previous_direction = current_direction

    def _forward_backward_or_out(self, location, direction):
        if self.directions[location] == direction:
            return self.FORWARD
        elif self.directions[location] == direction.opposite_direction():
            return self.BACKWARD
        else:
            return self.OUT
            

class Board:
    def __init__(self, paths: list[Path]):
        self.paths = paths


if __name__ == '__main__':
    unittest.main()
