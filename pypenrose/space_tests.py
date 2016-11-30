import itertools

import nose.tools
import numpy as np

from pypenrose.line import Parallel
import pypenrose.space as space


def test_basis_vecs():
    for x in range(100):
        basis = space.get_nd_basis(x)

        # Test unitary length
        extent = (np.asarray(basis)**2).sum(axis=1)
        assert np.allclose(extent, 1.0), extent


def test_gridlines():
    gl_list = space.get_1d_gridlines((0.5, 0.5), 0.0, 5)

    # All lines inside this list should be parallel
    for l1, l2 in itertools.permutations(gl_list, 2):
        with nose.tools.assert_raises(Parallel):
            l1.intersect(l2)


def test_line_list_generation():
    for ndim in range(5):
        space.get_nd_grid(1, ndim=ndim)
