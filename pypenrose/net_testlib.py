from pypenrose.line import get_1d_gridlines
from pypenrose.net import gridlines_to_gridgraph


def create_testing_net():
    horiz = get_1d_gridlines((1, 0), 0, 3)
    verti = get_1d_gridlines((0, 1), 0, 3)

    return gridlines_to_gridgraph(horiz + verti)
