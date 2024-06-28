import unittest
from board import *
from tileComponents import NORTH_FACING_PLANE, WEST_FACING_PLANE, SOUTH_FACING_PLANE, EAST_FACING_PLANE, COVERED


class TestSegmentMethods(unittest.TestCase):
    def test_from_points_length(self):
        for i, j in itertools.product(range(10), range(10)):
            if i == j:
                continue
            self.assertEqual(Segment.from_points(Point((0,i)), Point((0,j))).length, abs(i-j))
            self.assertEqual(Segment.from_points(Point((i,0)), Point((j,0))).length, abs(i - j))

    def test_from_points_zero_length(self):
        for i, j in itertools.product(range(10), range(10)):
            with self.assertRaises(ValueError):
                Segment.from_points(Point((i,j)),Point((i,j)))
    def test_from_points_diagonal(self):
        for i, j in itertools.product(range(1,10), range(1,10)):
            with self.assertRaises(ValueError):
                Segment.from_points(Point((0,0)), Point((i,j)))
    def test_from_points_north(self):
        self.assertEqual(Segment.from_points(Point((0,0)), Point((-2,0))).direction, NORTH)

    def test_from_points_west(self):
        self.assertEqual(Segment.from_points(Point((0,0)), Point((0,2))).direction, WEST)

    def test_from_points_south(self):
        self.assertEqual(Segment.from_points(Point((0,0)), Point((2,0))).direction, SOUTH)

    def test_from_points_east(self):
        self.assertEqual(Segment.from_points(Point((0,0)), Point((0,-2))).direction, EAST)


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
    DEFAULT_PATH = PathObjective.from_points([Point(c) for c in ((1, 1), (1, 4), (3, 4))])
    def test_path_from_points(self):
        path = PathObjective.from_points([Point(c) for c in ((1, 1), (3, 1), (3, 2), (1, 2))])
        self.assertEqual(path.locations, [Point(c) for c in ((1, 1), (2, 1), (3, 1), (3, 2), (2, 2), (1, 2))])

    def test_good_filling_gets_accepted(self):
        path = PathObjective.from_points([Point(c) for c in ((1, 1), (3, 1), (3, 2), (1, 2))])
        filling = PathFilling([COVERED, NORTH_FACING_PLANE, COVERED, COVERED, SOUTH_FACING_PLANE, COVERED])
        self.assertIsNone(path.raise_exception_if_filling_invalid(filling))

    def test_plane_not_along_path(self):
        path = PathObjective.from_points([Point(c) for c in ((1, 1), (3, 1), (3, 2))])
        filling = PathFilling([COVERED, NORTH_FACING_PLANE, COVERED, NORTH_FACING_PLANE])
        with self.assertRaises(PlaneDirectionException):
            path.raise_exception_if_filling_invalid(filling)

    def test_planes_in_different_directions(self):
        path = self.DEFAULT_PATH
        filling = PathFilling([COVERED, WEST_FACING_PLANE, COVERED, COVERED, NORTH_FACING_PLANE, COVERED])
        with self.assertRaises(PlaneDirectionException):
            path.raise_exception_if_filling_invalid(filling)

    def test_plane_on_corner(self):
        path = self.DEFAULT_PATH
        filling = PathFilling([COVERED, COVERED, COVERED, NORTH_FACING_PLANE, COVERED, COVERED])
        with self.assertRaises(PlaneLocationException):
            path.raise_exception_if_filling_invalid(filling)

    def test_plane_at_start_and_end(self):
        path = self.DEFAULT_PATH
        filling = PathFilling([WEST_FACING_PLANE, COVERED, COVERED, COVERED, COVERED, SOUTH_FACING_PLANE])
        self.assertIsNone(path.raise_exception_if_filling_invalid(filling))

    def test_bad_plane_at_end(self):
        path = self.DEFAULT_PATH
        filling = PathFilling([COVERED, COVERED, COVERED, COVERED, COVERED, WEST_FACING_PLANE])
        with self.assertRaises(PlaneDirectionException):
            path.raise_exception_if_filling_invalid(filling)

    def test_bad_plane_at_start(self):
        path = self.DEFAULT_PATH
        filling = PathFilling([SOUTH_FACING_PLANE, COVERED, COVERED, COVERED, COVERED, COVERED])
        with self.assertRaises(PlaneDirectionException):
            path.raise_exception_if_filling_invalid(filling)

    def test_directed_path_followed(self):
        path = self.DEFAULT_PATH
        path.flying_forward_mandatory = True
        filling = PathFilling([WEST_FACING_PLANE, COVERED, COVERED, COVERED, COVERED, SOUTH_FACING_PLANE])
        self.assertIsNone(path.raise_exception_if_filling_invalid(filling))

    def test_directed_path_not_followed(self):
        path = self.DEFAULT_PATH
        path.flying_forward_mandatory = True
        filling = PathFilling([EAST_FACING_PLANE, COVERED, COVERED, COVERED, COVERED, NORTH_FACING_PLANE])
        with self.assertRaises(PlaneDirectionException):
            path.raise_exception_if_filling_invalid(filling)

    def test_mandatory_planes_present(self):
        path = PathObjective.from_points([Point((50, 43)), Point((50, 50))], mandatory_planes=(0, 1, 2))
        filling = PathFilling(
            [WEST_FACING_PLANE, WEST_FACING_PLANE, WEST_FACING_PLANE, COVERED, COVERED, WEST_FACING_PLANE, COVERED, COVERED])
        self.assertIsNone(path.raise_exception_if_filling_invalid(filling))

    def test_mandatory_plane_missing(self):
        path = PathObjective.from_points([Point((50, 43)), Point((50, 50))], mandatory_planes=(0, 1, 2))
        filling = PathFilling([WEST_FACING_PLANE, COVERED, WEST_FACING_PLANE, COVERED, COVERED, WEST_FACING_PLANE, COVERED, COVERED])
        with self.assertRaises(MissingPlaneException):
            path.raise_exception_if_filling_invalid(filling)

    def test_filling_too_short(self):
        path = self.DEFAULT_PATH
        filling = PathFilling([])
        with self.assertRaises(FillingShapeError):
            path.raise_exception_if_filling_invalid(filling)

    def test_filling_too_long(self):
        path = self.DEFAULT_PATH
        filling = PathFilling([COVERED]*10)
        with self.assertRaises(FillingShapeError):
            path.raise_exception_if_filling_invalid(filling)

class TestBoardFillingMethods(unittest.TestCase):
    def test_indexing(self):
        filling = BoardFilling([[COVERED, WEST_FACING_PLANE, COVERED, SOUTH_FACING_PLANE],
                                [WEST_FACING_PLANE, COVERED, NORTH_FACING_PLANE, COVERED]])

        self.assertEqual(filling[Point((1, 1))], COVERED)
        self.assertEqual(filling[Point((1, 3))], COVERED)
        self.assertEqual(filling[Point((0, 1))], WEST_FACING_PLANE)

    def test_restriction_to_path(self):
        filling = BoardFilling([[WEST_FACING_PLANE, WEST_FACING_PLANE, COVERED, COVERED],
                                [COVERED, WEST_FACING_PLANE, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, SOUTH_FACING_PLANE],
                                [COVERED, COVERED, COVERED, COVERED]])
        path = Path.from_points([Point((0,0)), Point((0,3))])
        self.assertEqual(filling.restrict_to_path(path), PathFilling([WEST_FACING_PLANE, WEST_FACING_PLANE, COVERED, COVERED]))

class TestBoardObjectiveMethods(unittest.TestCase):
    DEFAULT_BOARD = BoardObjective([PathObjective.from_points([Point((1, 1)), Point((1, 3)), Point((3, 3))])], shape=(4, 4))
    def test_good_filling_passes(self):
        board = BoardObjective(
            [PathObjective.from_points([Point((1, 1)), Point((1, 3)), Point((3, 3))]),
             PathObjective.from_points([Point((0,0)), Point((0,3))])],
            shape=(4, 4))
        filling = BoardFilling([[WEST_FACING_PLANE, WEST_FACING_PLANE, COVERED, COVERED],
                                [COVERED, WEST_FACING_PLANE, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, SOUTH_FACING_PLANE],
                                [COVERED, COVERED, COVERED, COVERED]])
        self.assertIsNone(board.raise_exception_if_filling_invalid(filling))

    def test_crossing_paths(self):
        board = BoardObjective(
            [PathObjective.from_points([Point((0,1)), Point((2,1))]),PathObjective.from_points([Point((1,0)), Point((1,2))])],
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
            [PathObjective.from_points([Point((0, 1)), Point((2, 1))]),
             PathObjective.from_points([Point((0, 0)), Point((0, 1)), Point((2, 1)), Point((2, 0))])],
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
            [PathObjective.from_points([Point((3,3)), Point((1,3)), Point((1,1))], flying_forward_mandatory=True)],
            shape=(4, 4))
        filling = BoardFilling([[COVERED, COVERED, COVERED, COVERED],
                                [COVERED, WEST_FACING_PLANE, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED]])
        with self.assertRaises(PlaneDirectionException):
            board.raise_exception_if_filling_invalid(filling)

    def test_mandatory_planes_present(self):
        board = BoardObjective(
            [PathObjective.from_points([Point((0,0)), Point((0,3))], mandatory_planes=(0, 1, 2))],
            shape=(4, 4))
        filling = BoardFilling([[WEST_FACING_PLANE, WEST_FACING_PLANE, WEST_FACING_PLANE, COVERED],
                                [COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED],
                                [COVERED, COVERED, COVERED, COVERED]])
        self.assertIsNone(board.raise_exception_if_filling_invalid(filling))

    def test_mandatory_plane_missing(self):
        board = BoardObjective(
            [PathObjective.from_points([Point((0,0)), Point((0,3))], mandatory_planes=(0, 1, 2))],
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

    def test_from_string(self):
        board = self.DEFAULT_BOARD
        board_from_str = BoardObjective.from_string("    \n"+
                                                    " e>v\n"+
                                                    "   v\n"+
                                                    "   f")
        print(board_from_str.paths[0].locations)
        self.assertEqual(board, board_from_str)

    def test_eq(self):
        self.assertEqual(BoardObjective(
                             [PathObjective.from_points([Point((1, 1)), Point((1, 3)), Point((3, 3))]),
                              PathObjective.from_points([Point((1, 1)), Point((1, 3)), Point((0, 3))])],
                             shape=(4, 4)),
                         BoardObjective(
                             [PathObjective.from_points([Point((1, 1)), Point((1, 3)), Point((0, 3))]),
                              PathObjective.from_points([Point((1, 1)), Point((1, 3)), Point((3, 3))])],
                             shape=(4, 4)))

    def test_eq_different_shape(self):
        self.assertNotEqual(self.DEFAULT_BOARD,
                         BoardObjective(
                             [PathObjective.from_points([Point((1, 1)), Point((1, 3)), Point((3, 3))])],
                             shape=(4, 5)))


if __name__ == '__main__':
    unittest.main()
