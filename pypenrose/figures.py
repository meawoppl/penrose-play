from pypenrose.space import get_nd_basis
import pylab as plt


def draw_basis_figure(colors=["#FF9977", "brown", "red", "yellow", "green"]):
    for color, (xi, yi) in zip(colors, get_nd_basis(len(colors))):
        plt.plot([0, yi], [0, -xi], color, lw=6, alpha=0.7)

    plt.axis("equal")


def draw_three_and_five():
    plt.subplot(1, 2, 1)
    draw_basis_figure()
    plt.subplot(1, 2, 2)
    draw_basis_figure(["black"] * 3)


if __name__ == "__main__":
    plt.figure()
    draw_three_and_five()
    plt.show()
