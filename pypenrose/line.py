import numpy as np


class Parallel(RuntimeError):
    pass


class Colinear(Parallel):
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
            m = float(py2 - py1) / float(px2 - px1)
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

    def _vec(self):
        return np.asarray([self.x, self.y, self.i])

    # MRG TODO: Testme
    def parallel(self, other, eps=1e-6):
        # Compute the angle b/t the lines
        dot_prod = (self.x * other.x) + (self.y * other.y)
        s_mag = np.sqrt(self.x**2 + self.y**2)
        o_mag = np.sqrt(other.x**2 + other.y**2)

        # Constrain angle to q1 with abs
        deg = abs(dot_prod) / (s_mag * o_mag)
        return ((1 - abs(deg)) < eps)

    def normalized(self):
        n = np.max(np.abs(self._vec()))
        n *= np.sign(self.x)
        return Line(self.x / n, self.y / n, self.i / n)

    def equal(self, other, eps=1e-6):
        self_norm = self.normalized()._vec()
        othr_norm = other.normalized()._vec()

        return np.allclose(self_norm, othr_norm, atol=eps)

    def __eq__(self, other):
        return self.equal(other)

    def y_at(self, x_v):
        return Line(1, 0, x_v).intersect(self)[1]

    def x_at(self, y_v):
        return Line(0, 1, y_v).intersect(self)[0]

    def intersect(self, othr):
        assert isinstance(othr, Line)
        if self.parallel(othr):
            raise Parallel()

        mat = np.matrix(
            [[self.x, self.y],
             [othr.x, othr.y]])
        vec = np.matrix([self.i, othr.i]).T

        try:
            inv = mat.I
        except np.linalg.linalg.LinAlgError as e:
            raise Parallel() from e

        # Gross cohersion to tuple(x, y)
        return tuple(np.array((inv * vec)).flatten().tolist())

    def __str__(self):
        return "Line: %0.2fx + %0.2fy = %0.2f" % (self.x, self.y, self.i)
