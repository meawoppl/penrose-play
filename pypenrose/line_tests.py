import nose.tools

import pypenrose.line as line


def test_line_init():
    line.Line(1, 2, 3)
    line.Line(0, 2, 3)
    line.Line(1, 0, 3)

    # MRG: :/
    line.Line(0, 0, 0)


def test_line_init_invalid():
    with nose.tools.assert_raises(AssertionError):
        line.Line(float("inf"), 0, 0)

    with nose.tools.assert_raises(AssertionError):
        line.Line(0, float("nan"), 0)


def test_line_intercept():
    line1 = line.Line(0, 1, 1)
    line2 = line.Line(1, 0, 1)

    i1 = line1.intercept(line2)
    nose.tools.assert_equal(i1, (1, 1))


def test_line_intersect():
    line1 = line.Line(0, 1, 1)

    with nose.tools.assert_raises(line.Colinear):
        line1.intercept(line1)

    line3 = line.Line(1, -1, 1)
    line4 = line.Line(-1, 1, -1)
    with nose.tools.assert_raises(line.Colinear):
        line3.intercept(line4)

    with nose.tools.assert_raises(line.Colinear):
        line4.intercept(line3)


def test_line_string():
    line1 = line.Line(1, 1, 1)
    assert str(line1) == "Line: 1.00x + 1.00y = 1.00"
