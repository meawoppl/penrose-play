import numpy as np
import pylab as plt

from pypenrose.figures import plot_line_inside_bounds
import pypenrose.space as space


gl_list = space.get_1d_gridlines((0.5, 0.5), 0.0, 5)

# # All lines inside this list should be parallel
# for l1 in gl_list:
#     plot_line_inside_bounds(l1)
# plt.show()


# linesets = space.get_nd_grid(5, ndim=5)

# for lineset in linesets:
#     for line in lineset:
#         plot_line_inside_bounds(line)

# plt.show()


line_count = 9
xlines, ylines = space.get_nd_grid(line_count, ndim=2)

# Intersect all the parallel lines.
# Easy to test, none should intersect
xs, ys = space.dense_intersection(xlines, ylines)

for line in xlines + ylines:
    plot_line_inside_bounds(line)

for x, y in zip(xs.flatten(), ys.flatten()):
    plt.plot([x], [y], "bo", alpha=0.5)

plt.show()
