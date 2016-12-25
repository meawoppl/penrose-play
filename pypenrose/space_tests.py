import itertools

import nose.tools
import numpy as np

from pypenrose.line import Line, Parallel
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
    for n_vecs in range(1, 100):
        basis = space.get_nd_basis(n_vecs)
        nose.tools.assert_equal(len(basis), n_vecs)

        # Test unitary length
        extent = (np.asarray(basis)**2).sum(axis=1)
        assert np.allclose(extent, 1.0), extent


def test_gridlines():
    gl_list = space.get_1d_gridlines((0.5, 0.5), 0.0, 5)
    assert_all_lines_parallel(gl_list)


def test_line_list_generation():
    for ndim in range(5):
        grid_sets = space.get_nd_grid(1, ndim=ndim)
        nose.tools.assert_equal(len(grid_sets), ndim)


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


def test_grid_properties_offset_p1():
    groups = space.get_nd_grid_p1(6)

    # All lines with a group should be parallel.
    for n, group in enumerate(groups):
        assert_all_lines_parallel(group)

    # Each line from each group should interesect with
    # each line from each other group
    for g1, g2 in itertools.permutations(groups, 2):
        for l1, l2 in itertools.product(g1, g2):
            l1.intersect(l2)


def test_dense_intersection():
    line_count = 9
    xlines, ylines = space.get_nd_grid(line_count, ndim=2)

    # Intersect all the parallel lines.
    # Easy to test, none should intersect
    xys = space.dense_intersection(xlines, xlines)

    assert xys.shape == (2, line_count, line_count)
    assert np.all(np.isnan(xys))

    # The above should make unitary gridlines, so lets check them
    xs, ys = space.dense_intersection(xlines, ylines)

    # Self intersection should hit integer intersections for this pair
    for indx in range(0, line_count):
        assert np.allclose(xs[indx, :], indx - 4)
        assert np.allclose(ys[:, indx], indx - 4)


def test_dense_self_intersection():
    line_count = 5
    xlines, ylines = space.get_nd_grid(line_count, ndim=2)

    # Intersect all the parallel lines.
    # Easy to test, none should intersect
    xys = space.self_intersection(xlines)

    assert xys.shape == (2, line_count, line_count)
    assert np.all(np.isnan(xys))

    line_set = [Line(1, -1, 0), Line(1, 0, 1), Line(0, 1, 1)]

    xys = space.self_intersection(line_set)

    for x in range(len(line_set)):
        for y in range(len(line_set)):
            pt = xys[:, x, y]
            if x == y:
                assert np.all(np.isnan(pt))
            else:
                assert np.all(pt == 1)
