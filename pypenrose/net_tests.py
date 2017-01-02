import math

from mock import MagicMock
import nose.tools

from pypenrose.line import Line
import pypenrose.net
import pypenrose.net_testlib
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


def test_determine_winding():
    net = pypenrose.net_testlib.get_simple_net()
    center, edge_node = pypenrose.net_testlib.get_center_edge(net.g)

    winding = net.determine_winding(center, edge_node)
    nose.tools.assert_equal(len(winding), 4)
    nose.tools.assert_equal(
        winding[0],
        edge_node
    )

    for node in winding:
        nose.tools.assert_in(node, net.g)


def test_compute_angles():
    net = pypenrose.net_testlib.get_simple_net()
    center, edge_node = pypenrose.net_testlib.get_center_edge(net.g)

    # For the square mesh, all angles should be 90
    for angle in net.compute_angles(center, edge_node):
        nose.tools.assert_equal(angle, math.pi / 2)


def test_get_primary_spoke():
    net = pypenrose.net_testlib.get_simple_net()
    center, edge_node = pypenrose.net_testlib.get_center_edge(net.g)

    # Graph directions should point up in x and y
    # Y is CCW from X, so X sorts first
    spoke_node = net.get_primary_spoke(center)
    nose.tools.assert_equal(
        net.g.node[spoke_node]["intersection"],
        (1.0, 0.0)
    )


def test_draw_tile():
    # Pull out a node to draw from and the center
    net = pypenrose.net_testlib.get_simple_net()
    center, edge_node = pypenrose.net_testlib.get_center_edge(net.g)

    ctx_mock = MagicMock()
    line_to_mock = ctx_mock.rel_line_to

    net.draw_tile(ctx_mock, edge_node, center)

    # Should make 4 relative line calls
    nose.tools.assert_equal(line_to_mock.call_count, 4)

    # Line calls should close the graphing loop
    x_sum, y_sum = 0, 0
    for (dx, dy), _ in line_to_mock.call_args_list:
        x_sum += dx
        y_sum += dy

    nose.tools.assert_equal(x_sum, 0)
    nose.tools.assert_equal(y_sum, 0)


def test_get_line_root():
    # Pull out a node to draw from and the center
    net = pypenrose.net_testlib.get_simple_net()

    root_nodes = set()
    for line in net.lines:
        root_node = net.get_line_root(line)
        root_nodes.add(root_node)
    assert len(root_nodes) == 5
