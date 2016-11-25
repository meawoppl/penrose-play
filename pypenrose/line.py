import numpy as np


class Colinear(RuntimeError):
    pass


class Line:
    def __init__(self, x, y, i):
        assert np.all(np.isfinite((x, y, i))), "Not valid value for line"
        self.x = x
        self.y = y
        self.i = i

    def add_to_plot(plt):
        # Determine the plot extents
        # Determing where to draw lines within those extents
        # Draw the lines
        pass

    def intercept(self, othr):
        mat = np.matrix(
            [[self.x, self.y],
             [othr.x, othr.y]])
        vec = np.matrix([self.i, othr.i]).T

        try:
            inv = mat.I
        except np.linalg.linalg.LinAlgError as e:
            raise Colinear() from e

        # Gross cohersion to tuple(x, y)
        return tuple(np.array((inv * vec)).flatten().tolist())

    def __str__(self):
        return "Line: %0.2fx + %0.2fy = %0.2f" % (self.x, self.y, self.i)
