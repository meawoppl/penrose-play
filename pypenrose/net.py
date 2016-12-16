import itertools

import networkx as nx


def gridlines_to_gridgraph(list_of_gridlines):
	"""
	Turn N sets of gridlines into a nx-graph representing
	the connectivity of the intersections
	
	Arguments:
		list_of_gridlines {[type]} -- [description]
	
	Returns:
		[type] -- [description]
	"""
    g = nx.Graph()

    assert len(list_of_gridlines) >= 2

    for gl1, gl2 in itertools.permutation(list_of_gridlines):
        pass

    return g
