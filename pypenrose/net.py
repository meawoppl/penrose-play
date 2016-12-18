import networkx as nx

import pypenrose.line


def gridlines_to_gridgraph(list_of_gridlines):
    """
    Turn N sets of gridlines into a nx-graph where nodes represent
    an intersection between two lines (node-attrs) and edges connect
    nearest intersections.


    Arguments:
        list_of_lines {[Line(), Line()...]} --

    Returns:
        nx.Graph()
    """
    g = nx.Graph()

    for n1, line1 in enumerate(list_of_gridlines):
        intersecting = []
        for n2, line2 in enumerate(list_of_gridlines):
            # Skip self-self and previous comparisons (Upper matrix)
            if n2 >= n1:
                continue

            # No intersection for parallels
            try:
                xi, yi = line1.intersect(line2)
            except pypenrose.line.Parallel:
                continue

            intersecting.append((line2, xi, yi))

        # Now we sort the intersecting list on the "order" which they intersect
        ordered = list(sorted(intersecting, key=lambda lxy: line1.metric(lxy[1], lxy[2])))

        print("ORD", ordered)
        # Add all the intersections as nodes
        for line2, xi, yi in ordered:
            g.add_node((line1, line2), {"intersection": (xi, yi)})

        for i in range(len(ordered[:-1])):
            line2_1 = ordered[i][0]
            node1 = (line1, line2_1)

            line2_2 = ordered[i + 1][0]
            node2 = (line1, line2_2)

            g.add_edge(node1, node2)

    return g
