## /* Copyright 2007, Eyal Lotem, Noam Lewis, enoughmail@googlegroups.com */
## /*
##     This file is part of Enough.

##     Enough is free software; you can redistribute it and/or modify
##     it under the terms of the GNU General Public License as published by
##     the Free Software Foundation; either version 3 of the License, or
##     (at your option) any later version.

##     Enough is distributed in the hope that it will be useful,
##     but WITHOUT ANY WARRANTY; without even the implied warranty of
##     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##     GNU General Public License for more details.

##     You should have received a copy of the GNU General Public License
##     along with this program.  If not, see <http://www.gnu.org/licenses/>.
## */

import pygame
import math

from Widget import Widget
from Lib.Point import Point, from_polar, point_near_polyline
from guilib import MovingLine, paint_arrowhead_by_direction, rotate_surface


class NodeWidget(Widget):
    painting_z_order = 1 # these should always be painted AFTER edges
    def __init__(self, *args, **kw):
        super(NodeWidget, self).__init__(*args, **kw)
        self.out_edges = {}

    def entered_text(self, e):
        self.node.value.entered_text(e)
        
    def set_node(self, node):
        self.node = node
        node.value.widget = self

    def get_edges_to(self, other_widget):
        return self.out_edges.setdefault(other_widget, [])
    
    def add_edge(self, edge):
        other_widget = edge.target.value.widget
        line = MovingLine([self.center_pos().copy(),
                           other_widget.center_pos().copy()],
                          [self.center_pos(False).copy(),
                           other_widget.center_pos(False).copy()],
                          step=0.3)
        edge_widget = EdgeWidget(edge, line)
        self.get_edges_to(other_widget).append(edge_widget)
        return edge_widget

    def remove_edge(self, edge_widget):
        self.get_edges_to(edge_widget.target_widget).remove(edge_widget)
        

class EdgeWidget(Widget):
    painting_z_order = 0
    def __init__(self, edge, line, *args, **kw):
        super(EdgeWidget, self).__init__(*args, **kw)

        self.edge = edge
        self.target_widget = edge.target.value.widget
        self.line = line # A MovingLine
        self.text_pos = None

        self.params.back_color = (160, 10,10)
        self.params.text_color = (160, 10,10)
        self.params.focus_back_color = (250,80,80)
        self.params.focus_text_color = (250,80,80)
        self.params.hover_back_color = (220,30,30)
        self.params.hover_text_color = (220,30,30)

        # this is just to prevent the text size from changing. we
        # don't really care about the self.size NOR about self.pos
        self.params.autosize = "by text"

    def in_bounds(self, pos):
        return point_near_polyline(pos, self.line.current, 8)

    def entered_text(self, e):
        self.edge.value.entered_text(e)

    def update_from_dot(self, dot_edge, x_scale=1, y_scale=1, x_offset=0, y_offset=0, bezier_points=30):
        self.text_pos = Point((dot_edge['lx']*x_scale+x_offset, dot_edge['ly']*y_scale+y_offset))
        line = [Point((int(p[0]*x_scale+x_offset),
                       int(p[1]*y_scale+y_offset))) for p in dot_edge['points']]

        from Lib.Bezier import Bezier
        line.insert(0, (self.edge.source.value.widget.center_pos(False)))
        line.append((self.edge.target.value.widget.center_pos(False)))

        curve = Bezier(line, bezier_points)
        self.line.final = curve
        self.line.reset()
        
        
    def paint_shape(self, surface, back_color):
        shape = self.target_widget.get_shape()
        self.line.update()
        pygame.draw.lines(surface, back_color, False, [tuple(p) for p in self.line.current], 2)
        i = len(self.line.current)/2
        while i + 1 < len(self.line.current):
            a, b = self.line.current[i], self.line.current[i+1]
            i += 1
            for intersection in shape.intersections(a, b):
                break
            else:
                continue
            paint_arrowhead_by_direction(surface, (200,60,60), a, intersection)
            break

    def paint_text(self, surface):
        mid = len(self.line.current)/2
        midvalues = self.line.current[mid:mid+2]
        if len(midvalues) < 2:
            # not enough control points to figure out where to put text
            return
        midsrc, middst = midvalues
        angle = ((middst - midsrc).angle() % (2*math.pi))

        if 1*(2*math.pi)/4 < angle < 3*(2*math.pi)/4:
            angle += math.pi
            angle %= 2*math.pi

        t = self.rendered_text
        text_centering_vector = Point((-t.get_width()/2, -t.get_height()))
        text_centering_length = text_centering_vector.norm()
        text_centering_angle = text_centering_vector.angle()

        rt, coors = rotate_surface(t, angle)

        # coors[0] is where the original topleft is in the
        # rotated surface:
        topleft = coors[0]

        desired_topleft = midsrc + from_polar(text_centering_angle+angle,
                                              text_centering_length)
                
        pos = tuple(desired_topleft - topleft)
        surface.blit(rt, map(int, pos))

