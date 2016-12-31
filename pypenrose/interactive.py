import pylab as plt

from pypenrose.figures import plot_line_inside_bounds
import pypenrose.space
import pypenrose.net
import pypenrose.figures
import pypenrose.net_testlib


# Visual test for 1d grid
def show_gridlines():
    gl_list = pypenrose.space.get_1d_gridlines((0.5, 0.5), 0.0, 5)

    # All lines inside this list should be parallel
    for l1 in gl_list:
        plot_line_inside_bounds(l1)
    plt.show()


# Look at 5d gridlines
def show_nd_gridlines():
    linesets = pypenrose.space.get_nd_grid(5, ndim=5)
    for lineset in linesets:
        for line in lineset:
            plot_line_inside_bounds(line)

    plt.show()


# Plot the graph of P1
def plot_intersection_graph():
    lol_of_lines = pypenrose.space.get_nd_grid_p1(2)
    flat_lines = sum(lol_of_lines, [])

    line_isect_graph = pypenrose.net.gridlines_to_gridgraph(flat_lines)

    pypenrose.figures.plot_gridgraph(line_isect_graph)


pypenrose.figures.plot_gridgraph(
    pypenrose.net_testlib.get_simple_net()
)
