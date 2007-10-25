import twisted

from Lib import Graph
from functools import partial
from Lib.Dot import Dot, OutOfDate

class Layout(object):
    preserve_aspect_ratio = True
    def __init__(self):
        self.dot = Dot()
        
    def _out_of_date(self, failure):
        failure.trap(OutOfDate)
        return None

    def update(self, groups, size, node_widgets, edge_widgets, bezier_points = 30):
        d = Graph.get_drawing_data(self.dot, groups)
        d.addCallbacks(partial(self._layout, size, node_widgets, edge_widgets, bezier_points),
                       self._out_of_date)
        d.addErrback(twisted.python.log.err)

    def _layout(self, size, node_widgets, edge_widgets, bezier_points, (g, n, e)):
        if not n:
            return
        g_height, g_width = float(g['height']), float(g['width'])
        x_scale = size.x / g_width 
        y_scale = size.y / g_height
        x_offset = 0
        y_offset = 0
        if self.preserve_aspect_ratio:
            x_scale = y_scale = min(x_scale, y_scale)
            x_offset += (size.x - (x_scale * g_width)) / 2
            y_offset += (size.y - (y_scale * g_height)) / 2

        
        for node, n_layout in n.iteritems():
            widget = node_widgets[node]
            widget._pos.final.x = n_layout['x'] * x_scale + x_offset
            widget._pos.final.y = n_layout['y'] * y_scale + y_offset
            widget._size.final.x = n_layout['width'] * x_scale 
            widget._size.final.y = n_layout['height'] * y_scale
            widget._pos.final = widget._pos.final - widget._size.final * 0.5 
            widget._pos.reset()
            widget._size.reset()

        for node, n_layout in n.iteritems():
            lines = []
            if node not in e:
                continue
            last_indices = {}
            for edge, dot_edge in e[node].iteritems():
                widget = edge_widgets[edge]
                widget.update_from_dot(dot_edge,
                                       x_scale=x_scale,
                                       y_scale=y_scale,
                                       x_offset=x_offset,
                                       y_offset=y_offset,
                                       bezier_points=bezier_points)

