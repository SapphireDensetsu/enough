# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

import math
import pygame
from gui import draw
from guilib import MovingLine, paint_arrowhead_by_direction, rotate_surface, repaint_arrowhead, get_default
from Lib.Point import Point, from_polar, point_near_polyline
from gui.Widget import Widget

from gui.Keymap import Key, keydown_noarg

class EdgeWidget(Widget):
    bg_color=(150,10,10)
    fg_color=(150,30,30)
    activated_fg_color=(250,100,100)
    
    def __init__(self, edge, get_node_widget, line, *args, **kw):
        self.edge = edge
        self.get_node_widget = get_node_widget
        self.edge.obs.add_observer(self, '_edge_')
        Widget.__init__(self, *args, **kw)
        self.line = line
        self.draw_rect = None
        self.cached_arrowhead = None
        self.cached_parent_offset = None
        self.font = draw.get_font(pygame.font.get_default_font(), 14)
        self.rendered_text = self.font.render('', True, self.fg_color)

    def get_size(self):
        return self._size.current
    def set_size(self, p):
        raise NotImplementedError()
    size = property(get_size, set_size)

    def _edge_set_value(self, value):
        self.text = str(value)
        self.rendered_text = self.font.render(text, True, self.fg_color)

    def update(self):
        self.line.update()
        
    def in_bounds(self, pos):
        pos = Point(pos)
        dist = 8
        if self.draw_rect:
            if self.draw_rect.h < dist:
                self.draw_rect.y -= dist
                self.draw_rect.h += dist
            if self.draw_rect.w < dist:
                self.draw_rect.x -= dist
                self.draw_rect.w += dist
            if not self.draw_rect.collidepoint(tuple(pos)):
                return False
        return point_near_polyline(pos, self.line.current, dist)
        
    def update_from_dot(self, dot_edge, x_scale=1, y_scale=1, x_offset=0, y_offset=0, bezier_points=30):
        self.text_pos = Point((dot_edge['lx']*x_scale+x_offset, dot_edge['ly']*y_scale+y_offset))
        line = [Point((int(p[0]*x_scale+x_offset),
                       int(p[1]*y_scale+y_offset))) for p in dot_edge['points']]

        from Lib.Bezier import Bezier
        #line.insert(0, Point(self.get_node_widget(self.edge.source).rect().center))
        line.append(Point(self.get_node_widget(self.edge.target).final_rect().center))

        curve = Bezier(line, bezier_points)
        self.line.final = curve
        self.line.reset()
        
        
    def _draw(self, surface, parent_offset):
        self.paint_lines(surface, parent_offset)
        self.paint_text(surface, parent_offset)

    def paint_lines(self, surface, parent_offset):
        self.line.update()
        self.draw_rect = draw.lines(surface, self.bg_color, False, [tuple(p + parent_offset) for p in self.line.current], 2)

        target_widget = self.get_node_widget(self.edge.target)
        if (self.line.done and target_widget._pos.done and target_widget._size.done
            and self.cached_parent_offset and self.cached_parent_offset == parent_offset):
            changed = False
        else:
            changed = True
            self.cached_arrowhead = None
            
        if changed or not self.cached_arrowhead:
            # If we didn't cache the found intersection or some stuff changed....

            # TODO: make this a binary search 
            shape = target_widget.shape
            i = len(self.line.current)/2
            while i + 1 < len(self.line.current):
                a, b = self.line.current[i], self.line.current[i+1]
                i += 1
                for intersection in shape.intersections(a, b):
                    break
                else:
                    continue

                self.cached_arrowhead = paint_arrowhead_by_direction(surface, (200,60,60),
                                                                     a + parent_offset,
                                                                     intersection + parent_offset)
                self.cached_parent_offset = parent_offset
                return

        if self.cached_arrowhead:
            repaint_arrowhead(surface, *self.cached_arrowhead)
            

    def paint_text(self, surface, parent_offset):
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
                
        pos = tuple(desired_topleft - topleft + parent_offset)
        draw.blit(surface, rt, map(int, pos))

