import math

import nose.tools

from pypenrose.line import Line
import pypenrose.net
from pypenrose.net_testlib import assert_graph_props
import pypenrose.space


def test_net_graphgen_degenerate():
    # No lines to intersect
    g = pypenrose.net.gridlines_to_gridgraph([])
    assert_graph_props(g, nodes=0, edges=0)

    # Too few lines to intersect
    g = pypenrose.net.gridlines_to_gridgraph([Line(0, 1, 1)])
    assert_graph_props(g, nodes=0, edges=0)

    # All parallel lines
    g = pypenrose.net.gridlines_to_gridgraph([
        Line(0, 1, 1),
        Line(0, 1, 2),
        Line(0, 1, 3),
    ])
    assert_graph_props(g, nodes=0, edges=0)


def test_net_graphgen_1():
    # One intersection, no connected
    g = pypenrose.net.gridlines_to_gridgraph([
        Line(0, 1, 1),
        Line(1, 0, 1),
    ])
    assert_graph_props(g, nodes=1, edges=0)


def test_net_graphgen_2():
    # Two intersection, one connection
    g = pypenrose.net.gridlines_to_gridgraph([
        Line(0, 1, 1),
        Line(1, 0, 1),
        Line(1, 0, 2),
    ])
    assert_graph_props(g, nodes=2, edges=1)


def test_net_graphgen_3():
    # Triangle, 3 intersects, 3 edges
    g = pypenrose.net.gridlines_to_gridgraph([
        Line(1, 1, 0),
        Line(1, 0, 0),
        Line(0, 1, 1),
    ])
    assert_graph_props(g, nodes=3, edges=3)


def test_net_graphgen_5d():
    for line_count in range(1, 7):
        lol_of_lines = pypenrose.space.get_nd_grid_p1(line_count)

        all_lines = sum(lol_of_lines, [])
        g = pypenrose.net.gridlines_to_gridgraph(all_lines)

        expected_nodecount = 10 * line_count**2
        assert_graph_props(g, nodes=expected_nodecount)


def test_angle_between_nodes():
    nose.tools.assert_almost_equal(
        pypenrose.net.angle_between_nodes((1, 0), (0, 0), (0, 1)),
        math.pi / 2
    )

    nose.tools.assert_almost_equal(
        pypenrose.net.angle_between_nodes((0, 1), (0, 0), (1, 0)),
        -math.pi / 2
    )


def test_angle_between_nodes_degenerate():
    nose.tools.assert_equal(
        pypenrose.net.angle_between_nodes((0, 1), (0, 0), (0, 1)),
        0
    )

    # MRG NOTE: I really think this should be a NaN. (vs the c spec)
    # https://en.wikipedia.org/wiki/Atan2
    nose.tools.assert_equal(
        pypenrose.net.angle_between_nodes((0, 0), (0, 0), (0, 0)),
        0
    )
