from mock import MagicMock
import tempfile

import cairo
import nose.tools

from pypenrose.line import Line
import pypenrose.figures as figures
import pypenrose.net_testlib


def test_35():
    figures.draw_three_and_five()


def test_line_box_plot():
    line1 = Line(1, 1, 0)
    line2 = Line(1, -1, 0)

    figures.plot_line_inside_bounds(line1)
    figures.plot_line_inside_bounds(line2)


def test_PDFSurfaceWrapper():
    with tempfile.NamedTemporaryFile() as tf:
        with figures.PDFSurfaceWrapper(tf) as ctx:
            assert issubclass(ctx.__class__, cairo.Context)

        tf.seek(0)
        assert len(tf.read()) > 0, "No Bytes Written!"


def test_draw_tile():
    # Pull out a node to draw from and the center
    net = pypenrose.net_testlib.get_simple_net()
    center, edge_node = pypenrose.net_testlib.get_center_edge(net.g)

    ctx_mock = MagicMock()
    line_to_mock = ctx_mock.rel_line_to

    net.draw_tile(ctx_mock, edge_node, center)

    # Should make 4 relative line calls
    nose.tools.assert_equal(line_to_mock.call_count, 4)

    # Line calls should close the graphing loop
    x_sum, y_sum = 0, 0
    for (dx, dy), _ in line_to_mock.call_args_list:
        x_sum += dx
        y_sum += dy
    nose.tools.assert_equal(x_sum, 0)
    nose.tools.assert_equal(y_sum, 0)
