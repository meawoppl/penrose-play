import numpy as np
import scipy.spatial


class Net:
    def __init__(self, pts):
        self._p = np.asarray(pts)
        assert pts.ndim == 2, pts.ndim
        assert pts.shape[-1] == 2, pts.shape[-1]

        self._dt = scipy.spatial.Delaunay(self._p)

    def point_loop_iterator():
        pass
