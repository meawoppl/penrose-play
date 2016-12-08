import warnings

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

    # y extents
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
