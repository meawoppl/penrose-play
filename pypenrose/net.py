import networkx as nx

import pypenrose.line


def sort_lines_on_line(basis_line, other_lines):
    isects = [(line, basis_line.intersect(line)) for line in other_lines]

    isects_sorted = list(sorted(isects, key=lambda lxy: basis_line.metric(*lxy[1])))
    lines_sorted = list(sorted(isects, key=lambda lxy: basis_line.metric(*lxy[1])))

    return isects_sorted, lines_sorted


def ordered_line_pair(line1, line2):
    """Stable sort of two line instance for aggregation into a unique pair"""
    return tuple(sorted([line1, line2], key=lambda line: id(line)))


def gridlines_to_gridgraph(list_of_gridlines):
    """
    Turn N sets of gridlines into a nx-graph where nodes represent
    an intersection between two lines (node-attrs) and edges connect
    nearest intersections.


    Arguments:
        list_of_lines [Line(), Line()...] --

    Returns:
        nx.Graph()
    """
    g = nx.Graph()

    for n1, line1 in enumerate(list_of_gridlines):
        intersecting = []
        for n2, line2 in enumerate(list_of_gridlines):
            # No intersection for parallels
            try:
                xi, yi = line1.intersect(line2)
            except pypenrose.line.Parallel:
                continue

            intersecting.append((line2, xi, yi))

        # Now we sort the intersecting list on the "order" which they intersect
        ordered = list(sorted(intersecting, key=lambda lxy: line1.metric(lxy[1], lxy[2])))

        # Add all the intersections as nodes
        for line2, xi, yi in ordered:
            node = ordered_line_pair(line1, line2)
            g.add_node(node, {"intersection": (xi, yi)})

        for i in range(len(ordered[:-1])):
            line2_1 = ordered[i][0]
            node1 = ordered_line_pair(line1, line2_1)

            line2_2 = ordered[i + 1][0]
            node2 = ordered_line_pair(line1, line2_2)

            g.add_edge(node1, node2)

    return g
