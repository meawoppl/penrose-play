from pypenrose.line import Line
import pypenrose.figures as figures


def test_35():
    figures.draw_three_and_five()


def test_line_box_plot():
    line1 = Line(1, 1, 0)
    line2 = Line(1, -1, 0)

    figures.plot_line_inside_bounds(line1)
    figures.plot_line_inside_bounds(line2)
