import itertools

import nose.tools
import numpy as np

from pypenrose.line import Parallel
import pypenrose.space as space


def assert_all_lines_parallel(line_list):
    # All lines inside this list should be parallel
    for l1, l2 in itertools.permutations(line_list, 2):
        with nose.tools.assert_raises(Parallel):
            isect = l1.intersect(l2)
            print("Line collision", isect)
            print(l1.x, l1.y, l1.i)
            print(l2.x, l2.y, l2.i)


def assert_all_lines_intersect(line_list):
    for l1, l2 in itertools.permutations(line_list, 2):
        try:
            l1.intersect(l2)
        except Parallel as e:
            raise AssertionError from e


def test_basis_vecs():
    for x in range(100):
        basis = space.get_nd_basis(x)

        # Test unitary length
        extent = (np.asarray(basis)**2).sum(axis=1)
        assert np.allclose(extent, 1.0), extent


def test_gridlines():
    gl_list = space.get_1d_gridlines((0.5, 0.5), 0.0, 5)
    assert_all_lines_parallel(gl_list)


def test_line_list_generation():
    for ndim in range(5):
        space.get_nd_grid(1, ndim=ndim)


def test_grid_properties():
    groups = space.get_nd_grid(3, ndim=5)

    # All lines with a group should be parallel.
    for n, group in enumerate(groups):
        assert_all_lines_parallel(group)

    # Each line from each group should interesect with
    # each line from each other group
    for g1, g2 in itertools.permutations(groups, 2):
        for l1, l2 in itertools.product(g1, g2):
            l1.intersect(l2)


def test_grid_properties_offset():
    groups = space.get_nd_grid(3, ndim=5, offsets=np.random.uniform(0, 1, size=5))

    # All lines with a group should be parallel.
    for n, group in enumerate(groups):
        assert_all_lines_parallel(group)

    # Each line from each group should interesect with
    # each line from each other group
    for g1, g2 in itertools.permutations(groups, 2):
        for l1, l2 in itertools.product(g1, g2):
            l1.intersect(l2)
