import networkx as nx

import nose.tools

import pypenrose.net
from pypenrose.line import Line
import pypenrose.space


def assert_graph_props(g, *, nodes, edges):
    try:
        assert isinstance(g, nx.Graph)
        nose.tools.assert_equal(len(g.nodes()), nodes)
        nose.tools.assert_equal(len(g.edges()), edges)
    except AssertionError:
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

    # All parallell lines
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
