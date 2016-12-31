import math

import networkx as nx

import pypenrose.line
import pypenrose.util


def ordered_line_pair(line1, line2):
    """Stable sort of two line instance for aggregation into a unique pair"""
    return tuple(sorted([line1, line2], key=lambda line: id(line)))


def gridlines_to_gridgraph(list_of_gridlines):
    """
    Turn N sets of gridlines into a nx-graph where nodes represent
    an intersection between two lines (node-attrs) and edges connect
    nearest intersections.

    Arguments:
        list_of_lines [Line(), ... , Line()]

    Returns:
        nx.Graph()
    """
    g = nx.DiGraph()

    for line1 in list_of_gridlines:
        # Now we sort the intersecting list on the "order" which they intersect
        line_digraph = sorted_intersection_digraph(line1, list_of_gridlines)
        g = nx.compose(g, line_digraph)

    return g


def sorted_intersection_digraph(main_line, other_lines):
    """
    Return a list of tuples of the form (Line(), x_intersect, y_intersect)
    Tuples are in the order of the occurace along the line consistant with the .metric()
    function for the main_line

    Arguments:
        main_line -- An instance of Line()
        other_lines -- A list of Line() instances

    Returns:
        nx.DiGraph()
    """
    intersecting = []
    for other_line in other_lines:
        # No intersection for parallels
        try:
            xi, yi = main_line.intersect(other_line)
        except pypenrose.line.Parallel:
            continue

        intersecting.append((other_line, xi, yi))

    # Now we sort the intersecting list on the "order" which they intersect
    ordered = [line for line, x, y in sorted(intersecting, key=lambda lxy: main_line.metric(lxy[1], lxy[2]))]

    g = nx.DiGraph()
    # Add all the intersections as nodes
    for line2 in ordered:
        n = ordered_line_pair(main_line, line2)
        g.add_node(n, intersection=main_line.intersect(line2))

    for line1, line2 in zip(ordered[:-1], ordered[1:]):
        n1 = ordered_line_pair(main_line, line1)
        n2 = ordered_line_pair(main_line, line2)
        g.add_edge(n1, n2, line=main_line)

    return g


class Net:
    def __init__(self, list_of_lines):
        self.g = gridlines_to_gridgraph(list_of_lines)

    def _get_intersection(self, node):
        return self.g.node[node]["intersection"]

    def _angle_between_nodes(self, spoke_node, center_node, other_node):
        i1 = self._get_intersection(spoke_node)
        i2 = self._get_intersection(center_node)
        i3 = self._get_intersection(other_node)

        # Return the CCW angle between two points [0, 2pi)
        x1 = i1[0] - i2[0]
        y1 = i1[1] - i2[1]

        x2 = i3[0] - i2[0]
        y2 = i3[1] - i2[1]

        dot = x1 * x2 + y1 * y2      # dot product
        det = x1 * y2 - y1 * x2      # determinant

        val = math.atan2(det, dot)

        # [-180, 180) -> [0, 2pi)
        return val if val >= 0 else ((2 * math.pi) + val)

    def determine_winding(self, center_node, spoke_node):
        undirected = nx.Graph(self.g)
        neighbors = undirected.neighbors(center_node)
        assert spoke_node in neighbors, "Spoke node not connected to the center"

        def angle_wrt_to(other_node):
            return self._angle_between_nodes(spoke_node, center_node, other_node)

        return list(sorted(neighbors, key=angle_wrt_to))

    def compute_angles(self, center_node, spoke_node):
        winding = self.determine_winding(center_node, spoke_node)

        angles = []
        for n1, n2 in pypenrose.util.rolled_loop_iterator(winding):
            print(n1, n2)
            a = self._angle_between_nodes(n1, center_node, n2)
            angles.append(a)
        return angles
