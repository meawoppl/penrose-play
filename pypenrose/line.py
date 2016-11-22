import numpy as np


class Line:
    def __init__(self, x, y, i):
        self.x = x
        self.y = y
        self.i = i

    def add_to_plot():
        pass

    def intercept(self, othr):
        mat = np.matrix(
            [[self.x, self.y],
             [othr.x, othr.y]])
        vec = np.matrix((self.i, othr.i))

        return mat.I * vec
