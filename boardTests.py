import unittest
from board import *
from tiling import NORTH_FACING_PLANE, WEST_FACING_PLANE, SOUTH_FACING_PLANE, EAST_FACING_PLANE, COVERED


class TestSegmentMethods(unittest.TestCase):
    def test_from_points_length(self):
        for i, j in itertools.product(range(10), range(10)):
            if i == j:
                continue
            self.assertEqual(Segment.from_points((0,i), (0,j)).length, abs(i-j))
            self.assertEqual(Segment.from_points((i, 0), (j, 0)).length, abs(i - j))

    def test_from_points_zero_length(self):
        for i, j in itertools.product(range(10), range(10)):
            with self.assertRaises(ValueError):
                Segment.from_points((i,j),(i,j))
    def test_from_points_diagonal(self):
        for i, j in itertools.product(range(1,10), range(1,10)):
            with self.assertRaises(ValueError):
                Segment.from_points((0, 0), (i, j))
    def test_from_points_north(self):
        self.assertEqual(Segment.from_points((0,0), (-2, 0)).direction, NORTH)

    def test_from_points_west(self):
        self.assertEqual(Segment.from_points((0,0), (0, 2)).direction, WEST)

    def test_from_points_south(self):
        self.assertEqual(Segment.from_points((0,0), (2, 0)).direction, SOUTH)

    def test_from_points_east(self):
        self.assertEqual(Segment.from_points((0,0), (0, -2)).direction, EAST)


class TestPathFillingMethods(unittest.TestCase):
    def test_index(self):
        filling = PathFilling([COVERED, NORTH_FACING_PLANE, COVERED, COVERED, SOUTH_FACING_PLANE])
        self.assertEqual(filling[2], COVERED)
        self.assertEqual(filling[1], NORTH_FACING_PLANE)

    def test_enumerate(self):
        filling = PathFilling([WEST_FACING_PLANE, COVERED, COVERED, COVERED, COVERED, SOUTH_FACING_PLANE])
        self.assertEqual(list(filling.enumerate_just_the_planes()),
                         [(0,WEST_FACING_PLANE), (5, SOUTH_FACING_PLANE)])

        filling = PathFilling([WEST_FACING_PLANE, NORTH_FACING_PLANE, EAST_FACING_PLANE, COVERED, COVERED, SOUTH_FACING_PLANE])
        self.assertEqual(list(filling.enumerate_just_the_planes()),
                         [(0, WEST_FACING_PLANE), (1, NORTH_FACING_PLANE), (2, EAST_FACING_PLANE), (5, SOUTH_FACING_PLANE)])


class TestPathObjectiveMethods(unittest.TestCase):
    def test_path_from_points(self):
        path = PathObjective.from_points(((1, 1), (3, 1), (3, 2), (1, 2)))
        self.assertEqual(path.locations, [(1, 1), (2, 1), (3, 1), (3, 2), (2, 2), (1, 2)])

    def test_good_path_gets_accepted(self):
        path = PathObjective.from_points(((1, 1), (3, 1), (3, 2), (1, 2)))
        filling = PathFilling([COVERED, NORTH_FACING_PLANE, COVERED, COVERED, SOUTH_FACING_PLANE])
        self.assertIsNone(path.raise_exception_if_filling_invalid(filling))

    def test_plane_not_along_path(self):
        path = PathObjective.from_points(((1, 1), (3, 1), (3, 2)))
        filling = PathFilling([COVERED, NORTH_FACING_PLANE, COVERED, NORTH_FACING_PLANE])
        with self.assertRaises(PlaneDirectionException):
            path.raise_exception_if_filling_invalid(filling)

    def test_planes_in_different_directions(self):
        path = PathObjective.from_points(((1, 1), (3, 1), (3, 2)))
        filling = PathFilling([COVERED, NORTH_FACING_PLANE, COVERED, WEST_FACING_PLANE])
        with self.assertRaises(PlaneDirectionException):
            path.raise_exception_if_filling_invalid(filling)

    def test_plane_on_corner(self):
        path = PathObjective.from_points(((1, 1), (3, 1), (3, 2)))
        filling = PathFilling([COVERED, NORTH_FACING_PLANE, NORTH_FACING_PLANE, COVERED])
        with self.assertRaises(PlaneLocationException):
            path.raise_exception_if_filling_invalid(filling)

    def test_plane_at_start_and_end(self):
        path = PathObjective.from_points(((1, 1), (1, 4), (3, 4)))
        filling = PathFilling([WEST_FACING_PLANE, COVERED, COVERED, COVERED, COVERED, SOUTH_FACING_PLANE])
        self.assertIsNone(path.raise_exception_if_filling_invalid(filling))

    def test_bad_plane_at_end(self):
        path = PathObjective.from_points(((1, 1), (1, 4), (3, 4)))
        filling = PathFilling([COVERED, COVERED, COVERED, COVERED, COVERED, WEST_FACING_PLANE])
        with self.assertRaises(PlaneDirectionException):
            path.raise_exception_if_filling_invalid(filling)

    def test_bad_plane_at_start(self):
        path = PathObjective.from_points(((1, 1), (1, 4), (3, 4)))
        filling = PathFilling([SOUTH_FACING_PLANE, COVERED, COVERED, COVERED, COVERED, COVERED])
        with self.assertRaises(PlaneDirectionException):
            path.raise_exception_if_filling_invalid(filling)

    def test_directed_path_followed(self):
        path = PathObjective.from_points(((1, 1), (1, 4), (3, 4)), flying_forward_mandatory=True)
        filling = PathFilling([WEST_FACING_PLANE, COVERED, COVERED, COVERED, COVERED, SOUTH_FACING_PLANE])
        self.assertIsNone(path.raise_exception_if_filling_invalid(filling))

    def test_directed_path_not_followed(self):
        path = PathObjective.from_points(((3, 4), (1, 4), (1, 1)), flying_forward_mandatory=True)
        filling = PathFilling([WEST_FACING_PLANE, COVERED, COVERED, COVERED, COVERED, SOUTH_FACING_PLANE])
        with self.assertRaises(PlaneDirectionException):
            path.raise_exception_if_filling_invalid(filling)

    def test_mandatory_planes_present(self):
        path = PathObjective.from_points(((50, 43), (50, 50)), mandatory_planes=(0, 1, 2))
        filling = PathFilling(
            [WEST_FACING_PLANE, WEST_FACING_PLANE, WEST_FACING_PLANE, COVERED, COVERED, WEST_FACING_PLANE, COVERED, COVERED])
        self.assertIsNone(path.raise_exception_if_filling_invalid(filling))

    def test_mandatory_plane_missing(self):
        path = PathObjective.from_points(((50, 43), (50, 50)), mandatory_planes=(0, 1, 2))
        filling = PathFilling([WEST_FACING_PLANE, COVERED, WEST_FACING_PLANE, COVERED, COVERED, WEST_FACING_PLANE, COVERED, COVERED])
        with self.assertRaises(MissingPlaneException):
            path.raise_exception_if_filling_invalid(filling)


class TestBoardFillingMethods(unittest.TestCase):
    def test_indexing(self):
        filling = BoardFilling([[COVERED, WEST_FACING_PLANE, COVERED, SOUTH_FACING_PLANE],
                                [WEST_FACING_PLANE, COVERED, NORTH_FACING_PLANE, COVERED]])

        self.assertEqual(filling[1, 1], COVERED)
        self.assertEqual(filling[1, 3], COVERED)
        self.assertEqual(filling[0, 1], WEST_FACING_PLANE)

    def test_restriction_to_path(self):
        filling = BoardFilling([[WEST_FACING_PLANE, WEST_FACING_PLANE, COVERED, COVERED],
                                [COVERED, WEST_FACING_PLANE, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, SOUTH_FACING_PLANE],
                                [COVERED, COVERED, COVERED, COVERED]])
        path = Path.from_points(((0,0), (0,3)))
        print(filling.restrict_to_path(path))
        self.assertEqual(filling.restrict_to_path(path), PathFilling([WEST_FACING_PLANE, WEST_FACING_PLANE, COVERED, COVERED]))

class TestBoardObjectiveMethods(unittest.TestCase):
    DEFAULT_BOARD = BoardObjective((PathObjective.from_points(((1, 1), (1, 3), (3, 3))),), shape=(4, 4))
    def test_good_filling_passes(self):
        board = BoardObjective(
            (PathObjective.from_points(((3, 3), (1, 3), (1, 1))),
             PathObjective.from_points(((0,0), (0, 3)))),
            shape=(4, 4))
        filling = BoardFilling([[WEST_FACING_PLANE, WEST_FACING_PLANE, COVERED, COVERED],
                                [COVERED, WEST_FACING_PLANE, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, SOUTH_FACING_PLANE],
                                [COVERED, COVERED, COVERED, COVERED]])
        self.assertIsNone(board.raise_exception_if_filling_invalid(filling))

    def test_crossing_paths(self):
        board = BoardObjective(
            (PathObjective.from_points(((0, 1), (2,1))),PathObjective.from_points(((1, 0), (1,2)))),
            shape=(3, 3))
        filling = BoardFilling([[COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED]])

        self.assertIsNone(board.raise_exception_if_filling_invalid(filling))

        filling = BoardFilling([[COVERED, COVERED, COVERED],
                                [COVERED, WEST_FACING_PLANE, COVERED],
                                [COVERED, COVERED, COVERED]])
        with self.assertRaises(PlaneDirectionException):
            board.raise_exception_if_filling_invalid(filling)

    def test_parallel_overlapping_paths(self):
        board = BoardObjective(
            (PathObjective.from_points(((0, 1), (2, 1))),
             PathObjective.from_points(((0, 0), (0, 1), (2, 1), (2, 0)))),
             shape=(3,3))
        filling = BoardFilling([[COVERED, COVERED, COVERED],
                                [COVERED, SOUTH_FACING_PLANE, COVERED],
                                [COVERED, COVERED, COVERED]])

        self.assertIsNone(board.raise_exception_if_filling_invalid(filling))

    def test_plane_not_along_path(self):
        board = self.DEFAULT_BOARD
        filling = BoardFilling([[COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, SOUTH_FACING_PLANE, COVERED],
                                [COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED]])
        with self.assertRaises(PlaneDirectionException):
            board.raise_exception_if_filling_invalid(filling)

    def test_planes_in_different_directions(self):
        board = self.DEFAULT_BOARD
        filling = BoardFilling([[COVERED, COVERED, COVERED, COVERED],
                                [COVERED, WEST_FACING_PLANE, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, NORTH_FACING_PLANE],
                                [COVERED, COVERED, COVERED, COVERED]])
        with self.assertRaises(PlaneDirectionException):
            board.raise_exception_if_filling_invalid(filling)

    def test_plane_on_corner(self):
        board = self.DEFAULT_BOARD
        filling = BoardFilling([[COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, SOUTH_FACING_PLANE],
                                [COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED]])
        with self.assertRaises(PlaneLocationException):
            board.raise_exception_if_filling_invalid(filling)

    def test_plane_at_start_and_end(self):
        board = self.DEFAULT_BOARD
        filling = BoardFilling([[COVERED, COVERED, COVERED, COVERED],
                                [COVERED, EAST_FACING_PLANE, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, NORTH_FACING_PLANE]])
        self.assertIsNone(board.raise_exception_if_filling_invalid(filling))

    def test_bad_plane_at_end(self):
        board = self.DEFAULT_BOARD
        filling = BoardFilling([[COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, WEST_FACING_PLANE]])
        with self.assertRaises(PlaneDirectionException):
            board.raise_exception_if_filling_invalid(filling)

    def test_bad_plane_at_start(self):
        board = self.DEFAULT_BOARD
        filling = BoardFilling([[COVERED, COVERED, COVERED, COVERED],
                                [COVERED, NORTH_FACING_PLANE, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED]])
        with self.assertRaises(PlaneDirectionException):
            board.raise_exception_if_filling_invalid(filling)

    def test_directed_path_followed(self):
        board = self.DEFAULT_BOARD
        board.flying_forward_mandatory = True
        filling = BoardFilling([[COVERED, COVERED, COVERED, COVERED],
                                [COVERED, WEST_FACING_PLANE, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED]])
        self.assertIsNone(board.raise_exception_if_filling_invalid(filling))

    def test_directed_path_not_followed(self):
        board = BoardObjective(
            (PathObjective.from_points(((3, 3), (1, 3), (1, 1)), flying_forward_mandatory=True),),
            shape=(4, 4))
        filling = BoardFilling([[COVERED, COVERED, COVERED, COVERED],
                                [COVERED, WEST_FACING_PLANE, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED]])
        with self.assertRaises(PlaneDirectionException):
            board.raise_exception_if_filling_invalid(filling)

    def test_mandatory_planes_present(self):
        board = BoardObjective(
            (PathObjective.from_points(((0, 0), (0, 3)), mandatory_planes=(0, 1, 2)),),
            shape=(4, 4))
        filling = BoardFilling([[WEST_FACING_PLANE, WEST_FACING_PLANE, WEST_FACING_PLANE, COVERED],
                                [COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED]])
        self.assertIsNone(board.raise_exception_if_filling_invalid(filling))

    def test_mandatory_plane_missing(self):
        board = BoardObjective(
            (PathObjective.from_points(((0, 0), (0, 3)),mandatory_planes=(0, 1, 2),),),
            shape=(4, 4))
        filling = BoardFilling([[WEST_FACING_PLANE, COVERED, WEST_FACING_PLANE, COVERED],
                                [COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED]])
        with self.assertRaises(MissingPlaneException):
            board.raise_exception_if_filling_invalid(filling)

    def test_empty_filling_passes(self):
        board = self.DEFAULT_BOARD
        filling = BoardFilling([[COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED]])
        self.assertIsNone(board.raise_exception_if_filling_invalid(filling))
    def test_plane_outside_path(self):
        board = self.DEFAULT_BOARD
        filling = BoardFilling([[NORTH_FACING_PLANE, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED]])
        with self.assertRaises(PlaneLocationException):
            board.raise_exception_if_filling_invalid(filling)

    def test_filling_dimensions_too_small(self):
        board = self.DEFAULT_BOARD
        filling = BoardFilling([[]])

        with self.assertRaises(FillingShapeError):
            board.raise_exception_if_filling_invalid(filling)

    def test_filling_dimensions_too_big(self):
        board = self.DEFAULT_BOARD
        filling = BoardFilling([[COVERED, COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED, COVERED]])

        with self.assertRaises(FillingShapeError):
            board.raise_exception_if_filling_invalid(filling)

    def test_filling_dimensions_non_rectangular(self):
        with self.assertRaises(ValueError):
            BoardFilling([[COVERED, COVERED, COVERED, COVERED, COVERED],
                          [COVERED, COVERED, COVERED, COVERED, COVERED],
                          [COVERED, COVERED, COVERED, COVERED]])


if __name__ == '__main__':
    unittest.main()
