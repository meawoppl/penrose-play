import warnings

import cairo
import numpy as np
import pylab as plt

from pypenrose.line import Parallel
from pypenrose.space import get_nd_basis


def draw_basis_figure(colors=["#FF9977", "brown", "red", "yellow", "green"]):
    for color, (xi, yi) in zip(colors, get_nd_basis(len(colors))):
        plt.plot([0, yi], [0, -xi], color, lw=6, alpha=0.7)

    plt.axis("equal")


def draw_three_and_five():
    plt.subplot(1, 2, 1)
    draw_basis_figure()
    plt.subplot(1, 2, 2)
    draw_basis_figure(["black"] * 3)


def plot_line_inside_bounds(line, extents=[-10, 10, -10, 10], *plt_args, **plt_kwargs):
    pts = set()

    # X extents
    for extent in extents[0:2]:
        try:
            pt = line.y_at(extent)
        except Parallel:
            continue
        if pt > extents[2] and pt < extents[3]:
            pts.add((extent, pt))

    # Y extents
    for extent in extents[2:4]:
        try:
            pt = line.x_at(extent)
        except Parallel:
            continue
        if pt >= extents[0] and pt <= extents[1]:
            pts.add((pt, extent))

    if len(pts) != 2:
        warnings.warn("Line outside of cropping box")
        print(pts)
        return

    aray = pt1, pt2 = np.asarray(list(pts))
    plt.plot(aray[:, 0], aray[:, 1], *plt_args, **plt_kwargs)
    plt.axis(extents)


def plot_gridgraph(graph):
    # Draw points at the intersections
    for node, node_data in graph.nodes_iter(data=True):
        isect = node_data["intersection"]
        plt.plot([isect[0]], [isect[1]], "bo")

    for node1, node2 in graph.edges_iter():
        pt1 = graph.node[node1]["intersection"]
        pt2 = graph.node[node2]["intersection"]

        hull_edge = (graph.degree(node1) < 4) or (graph.degree(node2) < 4)

        color = "r" if hull_edge else "b"

        plt.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]], color=color, lw=3, alpha=.3)

    # for node, node_data in graph.nodes_iter(data=True):
    #     if graph.degree(node) == 4:
    #         draw_tile(graph, node)
    #     break

    plt.axis([-10, 10, -10, 10])
    plt.show()


def draw_tile(graph, node, from_node, ctx):
    surrounding = []
    for adj in graph[node]:
        s = graph.node[adj]["intersection"]
        surrounding.append(s)

    plt.plot()


class PDFSurfaceWrapper:
    def __init__(self, flo, inch_size=(10, 10)):
        self.__f = flo

        # MRG ? Why do I have to call the surface dims twice?
        self.surface = cairo.PDFSurface(self.__f, inch_size[0] * 72, inch_size[1] * 72)
        self.surface.set_size(inch_size[0] * 72, inch_size[1] * 72)

    def __enter__(self):
        return cairo.Context(self.surface)

    def __exit__(self, *args):
        self.surface.finish()
