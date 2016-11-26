import numpy as np


class Colinear(RuntimeError):
    pass


class Line:
    def __init__(self, x, y, i):
        assert np.all(np.isfinite((x, y, i))), "Not valid value for line"
        assert (x != 0) or (y != 0), "Not a valid equation"
        self.x = x
        self.y = y
        self.i = i

    @classmethod
    def from_two_points(cls, px1, py1, px2, py2):
        try:
            m = (py2 - py1) / (px2 - px1)
        except ZeroDivisionError:
            m = float("inf")

        return cls.from_point_slope(px1, py1, m)

    @classmethod
    def from_point_slope(cls, px, py, m):
        if m == float("inf"):
            return cls(1, 0, px)

        # (y-py) = m (x - px)
        # -m (x)  + y = - m (px) + py
        return cls(-m, 1, (-m * px) + py)

    def __eq__(self, other):
        # MRG NOTE this is wrong!!!
        try:
            self.intersect(other)
        except Colinear:
            return True
        return False

    def y_at(self, x_v):
        return Line(1, 0, x_v).intersect(self)[1]

    def x_at(self, y_v):
        return Line(0, 1, y_v).intersect(self)[0]

    def add_to_plot(plt, extents=(-10, 10, -10, 10)):
        # Determine the plot extents
        # Determing where to draw lines within those extents
        # Draw the lines
        pass

    def intersect(self, othr):
        assert isinstance(othr, Line)
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
