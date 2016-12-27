import networkx as nx

import nose.tools

import pypenrose.net
from pypenrose.line import Line
import pypenrose.space


def assert_graph_props(g, *, nodes=None, edges=None):
    try:
        assert isinstance(g, nx.Graph)
        if nodes is not None:
            nose.tools.assert_equal(len(g.nodes()), nodes, msg="Node Count Mismatch")
        if edges is not None:
            nose.tools.assert_equal(len(g.edges()), edges, msg="Edge Count Mismatch")
    except AssertionError:
        print()
        print("Your graphs appears fuckt")
        print("Nodes:")
        for node in g.nodes():
            print(node)
        print("Edges:")
        for edge in g.edges():
            print(edge)
        raise


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
