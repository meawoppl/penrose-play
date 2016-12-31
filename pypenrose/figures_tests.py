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
    center, edge_node = pypenrose.net_testlib.get_center_edge(net)

    ctx_mock = MagicMock()
    move_to_mock = ctx_mock.move_to
    line_to_mock = ctx_mock.line_to

    # figures.draw_tile(net, edge_node, center, ctx_mock)

    # nose.tools.assert_equal(line_to_mock.call_count, 4)
    # nose.tools.assert_equal(move_to_mock.call_count, 1)
