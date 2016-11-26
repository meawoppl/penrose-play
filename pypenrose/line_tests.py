import nose.tools

from pypenrose.line import Line, Colinear


def test_line_init():
    Line(1, 2, 3)
    Line(0, 2, 3)
    Line(1, 0, 3)

    with nose.tools.assert_raises(AssertionError):
        Line(0, 0, 0)

    with nose.tools.assert_raises(AssertionError):
        Line(0, 0, 45)

    with nose.tools.assert_raises(AssertionError):
        Line(float("inf"), 1, 3)


def test_line_init_invalid():
    with nose.tools.assert_raises(AssertionError):
        Line(float("inf"), 0, 0)

    with nose.tools.assert_raises(AssertionError):
        Line(0, float("nan"), 0)


def test_line_intercept():
    line1 = Line(0, 1, 1)
    line2 = Line(1, 0, 1)

    i1 = line1.intersect(line2)
    nose.tools.assert_equal(i1, (1, 1))


def test_line_intersect():
    line1 = Line(0, 1, 1)

    with nose.tools.assert_raises(Colinear):
        line1.intersect(line1)

    line3 = Line(1, -1, 1)
    line4 = Line(-1, 1, -1)
    with nose.tools.assert_raises(Colinear):
        line3.intersect(line4)

    with nose.tools.assert_raises(Colinear):
        line4.intersect(line3)


def test_line_string():
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


def test_alt_constructors():
    line1 = Line.from_point_slope(0, 0, 1)
    line2 = Line.from_two_points(0, 0, 1, 1)

    assert line1 == line2

    assert Line(1, 0, 1) == Line.from_point_slope(1, 0, float("inf"))
