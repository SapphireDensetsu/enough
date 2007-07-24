## /* Copyright 2007, Noam Lewis, enoughmail@googlegroups.com */
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
import random

from App import App, mouse_pos
from Widget import Widget
from Lib import Graph

from Lib.Point import Point

from guilib import get_default, MovingLine, paint_arrowhead_by_direction

class NodeValue(object):
    def __init__(self, name, start_pos=None):
        self.name = name
        self.start_pos = get_default(start_pos, Point(0,0))

    def set_widget(self, widget):
        self._widget = widget
        self.update_widget_text()
        self._widget.pos.final = self.start_pos
    def get_widget(self):
        return self._widget
    widget = property(fget=get_widget,fset=set_widget)
    
    def update_widget_text(self):
        self._widget.text = self.name

class GraphWidget(Widget):
    def __init__(self, *args, **kw):
        super(GraphWidget, self).__init__(*args, **kw)
        self.out_connection_lines = {}
        
    def set_node(self, node):
        self.node = node
        node.value.widget = self

    def connect_pos(self, upper=False):
        y = self.size.current.y * 0.5
        return self.pos.current + Point(self.size.current.x * 0.5, y)

    def iter_visible_nodes(self, nlist):
        for out_node in nlist:
            w = out_node.value.widget
            if not w.params.visible:
                continue
            yield w
    def iter_visible_connected(self, dir):
        for w in self.iter_visible_nodes(self.node.connections[dir]):
            yield w
            
    def paint_connections(self, surface):
        if self.node is None:
            return
        
        #for w in self.iter_visible_connected('in'):
        #    pygame.draw.aalines(surface, (200,20,50), False, (self.connect_pos().as_tuple(), w.connect_pos().as_tuple()), True)
        for other, lines in self.out_connection_lines.iteritems():
            for line in lines:
                line.update()
                pygame.draw.lines(surface, (200,20,50), False, [p.as_tuple() for p in line.current], 2)
                l = len(line.current)*1/4
                if l < 1: l = 1
                paint_arrowhead_by_direction(surface, (200,60,60), line.current[-l-1], line.current[-l])

        
class GraphApp(App):
    def __init__(self, *args, **kw):
        super(GraphApp, self).__init__(*args, **kw)
        from Lib.Dot import Dot
        self.dot = Dot()
        self.dragging_enabled = False
        self.connecting = False
        self.disconnecting = False
        self.pos_zoom = 1
        self.size_zoom = 0.9
        self.bezier_points = 30
        
    def add_nodes(self, nodes):
        for node in nodes:
            w = GraphWidget()
            w.set_node(node)
            self.add_widget(w)
        self.update_layout()            

    def zoom(self, zoom):
        self.pos_zoom *= zoom
        self.size_zoom *= zoom
        self.update_layout()

    def paint_connector(self, color):
        mpos = mouse_pos()
        cpos = self.focused_widget.center_pos()
        paint_arrowhead_by_direction(self.screen, color, cpos, mpos)
        pygame.draw.aalines(self.screen, color, False,
                            [cpos.as_tuple(), mpos.as_tuple()], True)
        
    def paint_widgets(self, event):
        for w in self.widgets:
            w.paint_connections(self.screen)
        super(GraphApp, self).paint_widgets(event)
        if self.connecting:
            self.paint_connector((150,250,150))
        if self.disconnecting:
            self.paint_connector((250,150,150))
            
        
    def _key_up(self, e):
        super(GraphApp, self)._key_up(e)
        if (e.mod & pygame.KMOD_CTRL):
            if e.key == pygame.K_w:
                self.zoom(1.3)
            elif e.key == pygame.K_q:
                self.zoom(1/(1.3))

            elif e.key == pygame.K_r:
                if not self.record:
                    self.start_record()
                else:
                    self.stop_record()

            elif e.key == pygame.K_a:
                n = []
                for i in xrange(1):
                    n1 = Graph.Node(NodeValue(str('new')))
                    n.append(n1)
                self.add_nodes(n)

            elif e.key == pygame.K_s:
                nodes = [widget.node for widget in self.widgets]
                print '\n'
                print Graph.generate_dot(nodes)
                print '\n'

            elif e.key == pygame.K_EQUALS:
                self.bezier_points += 3
                self.update_layout()
            elif e.key == pygame.K_MINUS:
                self.bezier_points -= 3
                if self.bezier_points < 4:
                    self.bezier_points = 4
                self.update_layout()

    def _mouse_down(self, e):
        super(GraphApp, self)._mouse_down(e)
        if self.focused_widget:
            if e.button == 1:
                self.connecting = True
                self.connecting_source = self.focused_widget.node
            elif e.button == 3:
                self.disconnecting = True
                self.disconnecting_source = self.focused_widget.node
                
    def _mouse_up(self, e):
        super(GraphApp, self)._mouse_up(e)
        if self.connecting:
            self.connecting = False
            target = self.focused_widget
            if target:
                self.connecting_source.connect_out(target.node)
                self.update_layout()
            self.connecting_source = None
        elif self.disconnecting:
            self.disconnecting = False
            target = self.focused_widget
            if target:
                if self.disconnecting_source.is_connected(target.node):
                    self.disconnecting_source.disconnect(target.node)
                    self.update_layout()
            self.disconnecting_source = None
            
            

    def update_layout(self):
        nodes = [widget.node for widget in self.widgets]
        g, n, e = Graph.get_drawing_data(self.dot, nodes)
        x_scale = self.width / float(g['width']) * self.pos_zoom
        y_scale = self.height / float(g['height']) * self.pos_zoom
        
        for node, n_layout in n.iteritems():
            node.value.widget.pos.final.x = n_layout['x'] * x_scale
            node.value.widget.pos.final.y = n_layout['y'] * y_scale
            node.value.widget.size.final.x = n_layout['width'] * x_scale * self.size_zoom
            node.value.widget.size.final.y = n_layout['height'] * y_scale * self.size_zoom
            node.value.widget.pos.final = node.value.widget.pos.final - node.value.widget.size.final * 0.5

        for node, n_layout in n.iteritems():
            lines = []
            previously_connected = list(node.value.widget.out_connection_lines.keys())
            if node in e:
                last_indices = {}
                for edge in e[node]:
                    this = node.value.widget
                    other = edge['head_node'].value.widget
                    if other in previously_connected:
                        previously_connected.remove(other)

                    line = [Point(int(p[0]*x_scale), int(p[1]*y_scale)) for p in edge['points']]
                    
                    from Lib.Bezier import Bezier
                    line.insert(0, (this.center_pos(False)))
                    line.append((other.center_pos(False)))
                    curve = Bezier(line, self.bezier_points)

                    connections = node.value.widget.out_connection_lines.setdefault(other, [])
                    # if there is more than one connection, we don't care to animate the correct one.
                    last_index = last_indices.setdefault(other, 0)
                    if len(connections) <= last_index:
                        connections.append(MovingLine([],[], step=0.5))
                    connections[last_index].final = curve
                    last_indices[other] += 1
                
            for other in previously_connected:
                del node.value.widget.out_connection_lines[other]
            
            

#---------------------------------------------


def test():
    a = GraphApp()

    import random
    random.seed(0)
    nodes = []
    for i in xrange(1):
        pos = Point(10*random.random() - 5, 10*random.random() - 5)
        pos = pos + Point(a.width, a.height)*0.5
        n1 = Graph.Node(NodeValue(str(i), pos))
        if nodes:
            n1.connect_out(random.choice(nodes))
            if (random.random() > 0.1):
                n1.connect_in(random.choice(nodes))
        nodes.append(n1)

    a.add_nodes(nodes)
    #a.start_record()
    a.run()

if __name__=='__main__':
    test()
