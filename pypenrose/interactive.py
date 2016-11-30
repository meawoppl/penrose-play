import pylab as plt

from pypenrose.figures import plot_line_inside_bounds
import pypenrose.space as space


linesets = space.get_nd_grid(5, ndim=5)


for lineset in linesets:
    for line in lineset:
        print(line)
        plot_line_inside_bounds(line)

plt.show()
