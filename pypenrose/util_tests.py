import nose.tools

import pypenrose.util


def test_roll_identity():
    for size in range(5):
        to_roll = list(range(size))

        nose.tools.assert_equal(
            pypenrose.util.roll(to_roll, 0),
            to_roll
        )

        nose.tools.assert_equal(
            pypenrose.util.roll(to_roll, len(to_roll)),
            to_roll
        )


def test_roll_basic():
    to_roll = [1, 2, 3, 4]

    nose.tools.assert_equal(
        pypenrose.util.roll(to_roll, 1),
        [2, 3, 4, 1]
    )

    nose.tools.assert_equal(
        pypenrose.util.roll(to_roll, 2),
        [3, 4, 1, 2]
    )


def test_roll_degenerate():
    for distance in range(5):
        nose.tools.assert_equal(
            pypenrose.util.roll([], distance),
            []
        )

        nose.tools.assert_equal(
            pypenrose.util.roll([1], distance),
            [1]
        )
