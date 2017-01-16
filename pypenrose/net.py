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
        self.lines = list_of_lines
        self.g = gridlines_to_gridgraph(self.lines)

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

    def _all_node_edges(self, node, data=False):
        ins = self.g.in_edges(nbunch=[node], data=data)
        outs = self.g.out_edges(nbunch=[node], data=data)
        return ins + outs

    def _node_degree(self, node):
        return len(self._all_node_edges(node))

    def get_node_on_line(self, line):
        # Go thru the edges, find a node on the line
        node_on_line = None
        for n1, n2, data in self.g.edges_iter(data=True):
            if data["line"] == line:
                node_on_line = n1
                break
        assert node_on_line is not None, "No edges found with assoicated Line()"
        return node_on_line

    def get_line_root(self, line, ctx=None):
        assert line in self.lines
        node_on_line = self.get_node_on_line(line)

        # Chase the found node to its base (MRG YUCKY)
        while True:
            incoming_edges = self.g.in_edges(nbunch=[node_on_line], data=True)
            parent_node = [n1 for n1, n2, data in incoming_edges if data["line"] == line]

            if ctx is not None:
                self.move_to_next_node(ctx, node_on_line, parent_node)

            if len(parent_node) == 0:
                return node_on_line
            node_on_line = parent_node[0]

    def determine_winding(self, center_node, spoke_node):
        undirected = nx.Graph(self.g)
        neighbors = undirected.neighbors(center_node)
        assert spoke_node in neighbors, "Spoke node not connected to the center"

        def angle_wrt_to(other_node):
            ang = self._angle_between_nodes(spoke_node, center_node, other_node)
            return ang

        wound = list(sorted(neighbors, key=angle_wrt_to))
        assert wound[0] == spoke_node, "Node order flummoxed."
        return wound

    def compute_angles(self, center_node, spoke_node):
        winding = self.determine_winding(center_node, spoke_node)

        angles = []
        for n1, n2 in pypenrose.util.rolled_loop_iterator(winding):
            a = self._angle_between_nodes(n1, center_node, n2)
            angles.append(a)
        return angles

    def get_primary_spoke(self, center_node):
        out_nodes = self.g.successors(center_node)
        assert len(out_nodes) == 2, "Missing spokes!"
        out1, out2 = out_nodes
        angle = self._angle_between_nodes(out1, center_node, out2)

        if angle < math.pi:
            return out1
        else:
            return out2

    def get_edge_dx_dy(self, node1, node2, normalize=True):
        """
        Arguments:
            node1 {[type]} -- A node in the networkx.Digraph self.g
            node2 {[type]} -- A node in the networkx.Digraph self.g

        Keyword Arguments:
            normalize {bool} -- Whether or not to normalize the diplacement (default: {True})

        Returns:
            (float, float) -- A tuple of Python floats describing the (x, y) dispacement
        """
        x1, y1 = self._get_intersection(node1)
        x2, y2 = self._get_intersection(node2)

        dx = x2 - x1
        dy = y2 - y1
        if normalize:
            mag = math.sqrt(dx**2 + dy**2)
            dx /= mag
            dy /= mag

        return dx, dy

    def draw_tile(self, ctx, from_node, tile_node):
        """
        Draw a rhombus based on the from node and to node

        Arguments:
            ctx cairo.Context -- A cairo drawing context with the current point where the drawing starts
            from_node {object} -- A node in the self.g networkx graph
            tile_node {[type]} -- A node in the self.g networkx graph
        """
        assert from_node in self.g, "Source nodes not in graph"
        assert tile_node in self.g, "Source nodes not in graph"

        # First line drawn crosses the from_node - tile_node edge
        ordered_nodes = pypenrose.util.roll(self.determine_winding(tile_node, from_node), 1)

        assert len(ordered_nodes) == 4
        assert ordered_nodes[-1] == from_node

        for n, (n1, n2) in enumerate(pypenrose.util.rolled_loop_iterator(ordered_nodes, 2)):
            dx, dy = self.get_edge_dx_dy(n1, n2)

            ctx.rel_line_to(dx, dy)

            if n == 0:
                pt = ctx.get_current_point()
        ctx.stroke()
        ctx.move_to(*pt)

    def _walk_line_edges(self, line):
        current_node = self.get_line_root(line)
        while True:
            # Find the next node in the list
            neighbors = [n2 for n1, n2, data in self.g.edges_iter(current_node, data=True) if data["line"] == line]

            # If there is no next node, we are done
            if len(neighbors) == 0:
                break

            next_node = neighbors[0]
            yield current_node, next_node

            current_node = next_node

    def move_to_next_node(self, ctx, n1, n2):
        dx, dy = self.get_edge_dx_dy(n1, n2)
        ctx.rel_move_to(dx, dy)

    def draw_dot(self, ctx, color=(1, 0, 0)):
        x, y = ctx.get_current_point()
        ctx.save()
        ctx.set_source_rgb(*color)
        ctx.arc(x, y, 0.1, 0, 2 * 3.141)
        ctx.stroke()
        ctx.restore()
        ctx.move_to(x, y)

    def draw_ribbon(self, ctx, line, debug_markers=False):
        for current_node, next_node in self._walk_line_edges(line):
            if self._node_degree(next_node) != 4:
                continue
            # Draw the tile
            if debug_markers:
                self.draw_dot(ctx, (1, 0, 0))

            self.draw_tile(ctx, current_node, next_node)

            if debug_markers:
                self.draw_dot(ctx, (0, 1, 0))

    def draw_tiling(self, ctx):
        pass
