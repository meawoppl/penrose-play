import nose.tools
import networkx as nx

import pypenrose.line
import pypenrose.net
from pypenrose.space import get_1d_gridlines


def assert_graph_props(g, *, nodes=None, edges=None):
    try:
        assert isinstance(g, nx.Graph)
        if nodes is not None:
            nose.tools.assert_equal(len(g.nodes()), nodes, msg="Node Count Mismatch")
        if edges is not None:
            nose.tools.assert_equal(len(g.edges()), edges, msg="Edge Count Mismatch")
    except AssertionError:
        print()
        print("Your graph shape is wrong:")
        print("Nodes:")
        for node in g.nodes():
            print(node)
        print("Edges:")
        for edge in g.edges():
            print(edge)
        raise

    # Check that the intersection points are 2 tuple of floats
    for node in g.nodes():
        intersection = g.node[node]["intersection"]
        assert len(intersection) == 2, intersection
        assert all(float(i) == i for i in intersection)

    # Check that all the edges get annotation of the parent line
    for node1, node2, data in g.edges(data=True):
        parent_line = data["line"]
        assert isinstance(parent_line, pypenrose.line.Line)


def get_simple_net(shape=(3, 3)):
    # This is a pure x-y edged net looking like this:
    #
    #   0-0-0
    #   | | |
    #   0-0-0
    #   | | |
    #   0-0-0

    horiz = get_1d_gridlines((1, 0), 0, shape[0])
    verti = get_1d_gridlines((0, 1), 0, shape[1])
    return pypenrose.net.Net(horiz + verti)


def get_center_edge(net):
    """
    Helper to return the first internal and
    edge node in a net it finds

    Arguments:
        net {nx.(Di)Graph} -- A nx graph representing a 2d net

    Returns:
        tuple(enclosed, edge) -- Two node identifiers

    Raises AssertionError if nodes with degree 3 and 4 are not found.
    """
    internal = None
    edge = None

    undirected = nx.Graph(net)
    for node, node_degree in undirected.degree_iter():
        if node_degree == 4:
            internal = node
        if node_degree == 3:
            edge = node
        if (internal is not None) and (edge is not None):
            break
    assert (internal is not None) and (edge is not None), "Net does not have correct topology"
    return internal, edge


def test_get_simple_net():
    n = get_simple_net()
    assert_graph_props(n.g, nodes=9, edges=12)
