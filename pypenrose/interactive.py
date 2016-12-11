import pylab as plt

from pypenrose.figures import plot_line_inside_bounds
import pypenrose.space as space


gl_list = space.get_1d_gridlines((0.5, 0.5), 0.0, 5)

# # All lines inside this list should be parallel
# for l1 in gl_list:
#     plot_line_inside_bounds(l1)
# plt.show()


linesets = space.get_nd_grid(5, ndim=2)

for lineset in linesets:
    for line in lineset:
        plot_line_inside_bounds(line)

plt.show()
