import cairo
import pylab as plt

import pypenrose.figures
import pypenrose.space
import pypenrose.net
import pypenrose.figures
import pypenrose.net_testlib


# Visual test for 1d grid
def show_gridlines():
    gl_list = pypenrose.space.get_1d_gridlines((0.5, 0.5), 0.0, 5)

    # All lines inside this list should be parallel
    for l1 in gl_list:
        pypenrose.figures.plot_line_inside_bounds(l1)
    plt.show()


# Look at 5d gridlines
def show_nd_gridlines():
    linesets = pypenrose.space.get_nd_grid(5, ndim=5)
    for lineset in linesets:
        for line in lineset:
            pypenrose.figures.plot_line_inside_bounds(line)

    plt.show()


# Plot the graph of P1
def plot_intersection_graph():
    lol_of_lines = pypenrose.space.get_nd_grid_p1(5)
    flat_lines = sum(lol_of_lines, [])

    net = pypenrose.net.Net(flat_lines)

    pypenrose.figures.plot_gridgraph(net.g)

# plot_intersection_graph()


def draw_tile():
    # Pull out a node to draw from and the center
    net = pypenrose.net_testlib.get_simple_net()
    center, edge_node = pypenrose.net_testlib.get_center_edge(net.g)

    f = open("test.pdf", "wb")
    with pypenrose.figures.PDFSurfaceWrapper(f) as ctx:
        ctx.move_to(0, 0)
        ctx.set_source_rgba(0, 0, 0, 0.5)
        ctx.scale(20, 20)
        net.draw_tile(ctx, edge_node, center)
        ctx.stroke()


def draw_ribbon():
    lol_of_lines = pypenrose.space.get_nd_grid_m1(7)
    flat_lines = sum(lol_of_lines, [])

    net = pypenrose.net.Net(flat_lines)

    # net = pypenrose.net_testlib.get_simple_net(shape=(3, 5))
    # line = net.lines[1]

    f = open("test.pdf", "wb")
    with pypenrose.figures.PDFSurfaceWrapper(f) as ctx:
        ctx.move_to(300, 300)
        ctx.set_source_rgba(0, 0, 1, 0.3)
        ctx.set_line_width(0.1)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.scale(10, 10)
        for n, line in enumerate(net.lines):
            # ctx.set_line_width(0.1 * ((n+1)*2))
            ctx.move_to(30, 30)
            net.draw_ribbon(ctx, line)

        ctx.stroke()

draw_ribbon()
