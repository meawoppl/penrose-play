import numpy as np

from pypenrose.line import Line, Parallel


def get_nd_basis(n=5):
    """
    Generate the basis vectors for a n-dimensional grid viewed isometrically.
    """
    assert n >= 0
    t = np.linspace(0, 2 * np.pi, n + 1)[:-1]
    xs = np.cos(t)
    ys = np.sin(t)
    return [(x, y) for x, y in zip(xs, ys)]


def get_1d_gridlines(xy, offset, line_count):
    assert (0 <= abs(offset)) and (abs(offset) <= 1)

    lines = []
    for n in range(line_count):
        # point on the line normal from the origin
        x1 = xy[0] * (n + offset - ((line_count - 1) / 2))
        y1 = xy[1] * (n + offset - ((line_count - 1) / 2))

        # Point one step normal
        x2 = x1 + xy[1]
        y2 = y1 - xy[0]

        lines.append(Line.from_two_points(x1, y1, x2, y2))
    return lines


def get_nd_grid(n_lines, ndim=5, offsets=None):
    if offsets is None:
        offsets = [0.0] * ndim

    lines_lists = []
    for basis, offset in zip(get_nd_basis(n=ndim), offsets):
        lines = get_1d_gridlines(basis, offset, n_lines)
        lines_lists.append(lines)

    return lines_lists


def get_nd_grid_p1(n_lines):
    t2 = +(np.sqrt(5) - 1) / 4
    t3 = -(np.sqrt(5) + 1) / 4
    t4 = +(np.sqrt(5) - 1) / 4
    t5 = -(np.sqrt(5) + 1) / 4

    v = (1, t2, t3, t4, t5)

    return get_nd_grid(n_lines, ndim=5, offsets=v)


def dense_intersection(lines1, lines2):
    out_shape = (2, len(lines1), len(lines2))
    output = np.zeros(out_shape, dtype=np.float64)

    for lid1, line1 in enumerate(lines1):
        for lid2, line2 in enumerate(lines2):
            if lid2 < lid1:
                continue
            try:
                result = line1.intersect(line2)
            except Parallel:
                result = (np.nan, np.nan)

            output[:, lid1, lid2] = result
            output[:, lid2, lid1] = result

    return output


# def intersect_all_gridlines(line_sets):
#     assert len(line_sets) >= 0

#     for gid1, set1 in enumerate(line_sets):
#         for gid2, set2 in enumerate(line_sets):
#             # Only do the upper diag
#             if gid2 <= gid1:
#                 continue
#             dense_intersection(set1, set2)
