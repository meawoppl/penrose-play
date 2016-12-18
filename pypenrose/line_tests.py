import nose.tools

import numpy as np

from pypenrose.line import Line, Parallel


def test_init():
    Line(1, 2, 3)
    Line(0, 2, 3)
    Line(1, 0, 3)

    with nose.tools.assert_raises(AssertionError):
        Line(0, 0, 0)

    with nose.tools.assert_raises(AssertionError):
        Line(0, 0, 45)

    with nose.tools.assert_raises(AssertionError):
        Line(float("inf"), 1, 3)


def test_init_invalid():
    with nose.tools.assert_raises(AssertionError):
        Line(float("inf"), 0, 0)

    with nose.tools.assert_raises(AssertionError):
        Line(0, float("nan"), 0)


def test_intersect():
    line1 = Line(0, 1, 1)
    line2 = Line(1, 0, 1)

    i1 = line1.intersect(line2)
    nose.tools.assert_equal(i1, (1, 1))


def test_intersect_colinear():
    line1 = Line(0, 1, 1)

    with nose.tools.assert_raises(Parallel):
        line1.intersect(line1)

    line3 = Line(1, -1, 1)
    line4 = Line(-1, 1, -1)
    with nose.tools.assert_raises(Parallel):
        line3.intersect(line4)

    with nose.tools.assert_raises(Parallel):
        line4.intersect(line3)


def test_intersect_parallel_harder():
    line1 = Line(1.38, 1.00, -0.00)

    for incr in np.linspace(0, 0.000000001, 100):
        with nose.tools.assert_raises(Parallel):
            line2 = Line(1.38 + incr, 1.00, 0.0)
            line1.intersect(line2)


def test_string():
    line1 = Line(1, 1, 1)
    assert str(line1) == "Line: 1.00x + 1.00y = 1.00"


def test_eval():
    line1 = Line(1, -1, 0)  # y = x
    assert line1.x_at(5) == 5, line1.x_at(5)
    assert line1.y_at(5) == 5, line1.y_at(5)


def test_eq_operator():
    line1 = Line(1, -1, 0)  # y = x
    line2 = Line(-1, 1, 0)  # y = x

    assert line1 == line2
    assert line2 == line1

    line3 = Line(5, 4, 3)
    line4 = Line(-1, 3, 7)

    assert line3 != line4

    # Parallel but not equal
    line5 = Line(1, 1, 1)
    line6 = Line(1, 1, 2)

    assert line5 != line6


def test_alt_constructors():
    line1 = Line.from_point_slope(0, 0, 1)
    line2 = Line.from_two_points(0, 0, 1, 1)

    assert line1 == line2
    assert Line(1, 0, 1) == Line.from_point_slope(1, 0, float("inf"))

    line3 = Line.from_two_points(0.0, 0.0, 0.0, -1.0)
    line4 = Line.from_two_points(0.0, 0.0, 0.0, 1.0)

    with nose.tools.assert_raises(Parallel):
        line3.intersect(line4)


def test_closest_point_to():
    line1 = Line.from_two_points(0, 0, 1, 1)
    ptx, pty = line1.closest_point_to(0, 1)

    assert np.allclose([ptx, pty], 0.5)


def test_distance_to():
    line1 = Line.from_two_points(0, 0, 1, 1)

    for i in range(5):
        assert np.allclose(line1.distance_to(i, i), 0)

    assert np.allclose(line1.distance_to(1, 0), np.sqrt(2) / 2)
    assert np.allclose(line1.distance_to(0, 1), np.sqrt(2) / 2)


def test_normal_line_through():
    line1 = Line.from_two_points(0, 0, 1, 1)
    line2 = line1.normal_line_through(0, 0)

    xi, yi = line1.intersect(line2)
    assert np.allclose([xi, yi], 0)

    # Test normals to x=1
    line3 = Line(1, 0, 0)
    line4 = line3.normal_line_through(0, 0)
    print(line4)
    line5 = line4.normal_line_through(0, 0)
    assert line3 == line5, str(line3) + "!=" + str(line5)

    # Test normals to y=1
    line6 = Line(0, 1, 0)
    line7 = line6.normal_line_through(0, 0)
    line8 = line7.normal_line_through(0, 0)
    assert line8 == line6


def test_signed_distance_manhattan():
    line1 = Line.from_two_points(0, 0, 1, 1)

    for i in range(5):
        # Pts on the line
        nose.tools.assert_equal(line1.signed_distance_manhattan(i, i), 0)

        # Pts one unit above/below
        nose.tools.assert_equal(line1.signed_distance_manhattan(i + 1, i), 1)
        nose.tools.assert_equal(line1.signed_distance_manhattan(i - 1, i), -1)

        nose.tools.assert_equal(line1.signed_distance_manhattan(i, i + 1), -1)
        nose.tools.assert_equal(line1.signed_distance_manhattan(i, i - 1), 1)


def test_line_signed_distance_euclidean():
    line1 = Line.from_two_points(0, 0, 1, 1)

    for i in range(5):
        nose.tools.assert_equal(line1.signed_distance_euclidean(i, i), 0)

        nose.tools.assert_equal(line1.signed_distance_euclidean(i, i + 1), -np.sqrt(2) / 2)
        nose.tools.assert_equal(line1.signed_distance_euclidean(i, i - 1), np.sqrt(2) / 2)

        nose.tools.assert_equal(line1.signed_distance_euclidean(i + 1, i), np.sqrt(2) / 2)
        nose.tools.assert_equal(line1.signed_distance_euclidean(i - 1, i), -np.sqrt(2) / 2)


def test_line_metric():
    line1 = Line.from_two_points(0, 0, 1, 1)

    for i in range(5):
        r = line1.metric(i, i)
        assert np.allclose(r, np.sqrt(2) * i)

        r = line1.metric(-i, -i)
        assert np.allclose(r, -np.sqrt(2) * i)

        r = line1.metric(i, -i)
        assert np.allclose(r, 0)

        r = line1.metric(-i, i)
        assert np.allclose(r, 0)
