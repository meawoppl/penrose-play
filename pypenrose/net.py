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


def sorted_intersection_list(main_line, other_lines):
    """
    Return a list of tuples of the form (Line(), x_intersect, y_intersect)
    Tuples are in the order of the occurace along the line consistant with the .metric()
    function for the main_line

    Arguments:
        main_line -- An instance of Line()
        other_lines -- A list of Line() instances

    Returns:
        [(Line_1, x_1, y_1) ... (Line_n, x_n, y_n)]
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
    return [line for line, x, y in sorted(intersecting, key=lambda lxy: main_line.metric(lxy[1], lxy[2]))]


def sorted_intersection_digraph(main_line, other_lines):
    ordered = sorted_intersection_list(main_line, other_lines)

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
