import numpy as np


def generate_starting_vectors():
    t = np.linspace(0, 2 * np.pi, 5)
    xs = np.cos(t)
    ys = np.sin(t)
    return (xs, ys)


def get_basis_grid(n_lines, offsets=[0, 0, 0, 0, 0]):
    offsets = np.asarray(offsets)
    eqs = {}

    xs, ys = generate_starting_vectors()
    for xd, yd, offset in zip(xs, ys, offsets):
        eqs[xd, yd] = np.arange(n_lines) - offset
    return eqs


def iter_eqtns(equation_list):
    for (x, y), ints in equation_list.items():
        for i in ints:
            yield x, y, i


def iter_eqtns_upper(equation_list):
    # MRG TODO: Super gross
    for (x1, y1), ints1 in equation_list.items():
        for i1 in ints1:
            for (x2, y2), ints2 in equation_list.items():
                if x1 == x2 and y1 == y2:
                    continue
                for i2 in ints2:
                    yield (x1, y1, i1), (x2, y2, i2)


def plot_basis_grid():
    eqs = get_basis_grid(5)
    for eq1, eq2 in iter_eqtns_upper(eqs):
        print(eq1, eq2)

plot_basis_grid()
