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

from functools import partial
import pygame
import time

import twisted.python.log

from App import App, mouse_pos
from Widget import Widget
from Lib import Graph
from Lib.Dot import Dot, OutOfDate
from Lib.Font import get_font
from Lib.Point import Point

from guilib import get_default, MovingLine, paint_arrowhead_by_direction, pygame_reverse_key_map, rotate_surface

class NodeValue(object):
    def __init__(self, name, group_name = None, start_pos=None):
        self.name = name
        self.group_name = group_name
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

    def entered_text(self, event):
        import string
        if event.key == pygame.K_BACKSPACE:
            self.name = self.name[:-1]
        elif event.unicode in string.printable:
            self.name += event.unicode.replace('\r', '\n')
        self.update_widget_text()

    def get_node_properties(self):
        name_text = repr(str(self.name))[1:-1] # Str translates unicode to regular strings
        return {'label': '"%s"' % (name_text,),
                }

class NodeWidget(Widget):
    painting_z_order = 1 # these should always be painted AFTER edges
    def __init__(self, *args, **kw):
        super(NodeWidget, self).__init__(*args, **kw)
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

    def get_connection_lines_to(self, other_widget):
        return self.out_connection_lines.setdefault(other_widget, [])
    
    def add_edge(self, other_widget):
        line = MovingLine([self.center_pos().copy(),
                           other_widget.center_pos().copy()],
                          [self.center_pos(False).copy(),
                           other_widget.center_pos(False).copy()],
                          step=0.5)
        edge_widget = EdgeWidget(other_widget, line)
        self.get_connection_lines_to(other_widget).append(edge_widget)
        return edge_widget
        
##    def paint_connections(self, surface):
##        if self.node is None:
##            return

##                text = 'test text'
##                t = get_font(35).render(text, True, (255, 0, 0))
                
##                angle = (c[1] - c[0]).angle()

##                import math
##                if 1*(2*math.pi)/4 < angle < 3*(2*math.pi)/4:
##                    angle += math.pi
##                    angle %= 2*math.pi

##                text_centering_vector = Point(-t.get_width()/2, -t.get_height())
##                text_centering_length = text_centering_vector.norm()
##                text_centering_angle = text_centering_vector.angle()

##                rt, coors = rotate_surface(t, angle)

##                # coors[0] is where the original topleft is in the
##                # rotated surface:
##                topleft = coors[0]

##                desired_topleft = c[0] + Point.from_polar(text_centering_angle+angle,
##                                                          text_centering_length)
                
##                pos = (desired_topleft - topleft).as_tuple()
##                surface.blit(rt, map(int, pos))

class EdgeWidget(Widget):
    painting_z_order = 0
    def __init__(self, target, line, *args, **kw):
        super(EdgeWidget, self).__init__(*args, **kw)

        self.target = target
        self.line = line # A MovingLine
        
    def paint_shape(self, surface, back_color):
        shape = self.target.get_shape()
        self.line.update()
        pygame.draw.lines(surface, (200,20,50), False, [p.as_tuple() for p in self.line.current], 2)
        c = self.line.current[len(self.line.current)/2:]
        for a, b in zip(c, c[1:]):
            for intersection in shape.intersections(a, b):
                break
            else:
                continue
            paint_arrowhead_by_direction(surface, (200,60,60), a, intersection)
            break
        
    
def undoable_method(func):
    def new_func(self, *args, **kw):
        undoer = func(self, *args, **kw)
        if self.undoing:
            l = self.history_redo
        else:
            l = self.history
        if len(l) < self.max_undo:
            l.append((func, undoer, args, kw))
    return new_func
    
class GraphApp(App):
    def __init__(self, *args, **kw):
        super(GraphApp, self).__init__(*args, **kw)
        self.dot = Dot()
        self.init_control_map()
        
        self.dragging_enabled = False
        self.connecting = False
        self.disconnecting = False
        self.pos_zoom = 1
        self.size_zoom = 0.8
        self.bezier_points = 30
        self.modal_nodes = None
        
        self.history = []
        self.history_redo = []
        self.undoing = False
        self.max_undo = 25
        
        self.dot_prog_num = 0
        
        self.status_font = pygame.font.SysFont('serif',self.height/20)
        self.rendered_status_texts = []
        self.show_help()
        
    def init_control_map(self):
        zoom_amount = 1.3
        self.control_map = {pygame.K_w: ("Zoom in", partial(self.zoom, zoom_amount)),
                            pygame.K_q: ("Zoom out", partial(self.zoom, 1.0/zoom_amount)),
                            pygame.K_z: ("Undo", self.undo),
                            pygame.K_y: ("Redo", self.redo),
                            pygame.K_r: ("Record (toggle)", self.toggle_record),
                            pygame.K_a: ("Create new node", self.create_new_node),
                            pygame.K_d: ("Delete selected nodes", self.delete_selected_nodes),
                            pygame.K_s: ("Output DOT description", self.output_dot_description),
                            pygame.K_EQUALS: ("Higher curve resolution", partial(self.change_curve_resolution,
                                                                                 3)),
                            pygame.K_MINUS: ("Lower curve resolution", partial(self.change_curve_resolution,
                                                                               -3)),
                            pygame.K_h: ("Show help", self.show_help),
                            pygame.K_F1:("Show help", self.show_help),
                            pygame.K_l: ("Switch layout engine", partial(self.toggle_layout_engine, 1)),
                            }

    @undoable_method
    def add_nodes(self, nodes):
        self.set_status_text("Add %d nodes" % (len(nodes),))
        for node in nodes:
            w = NodeWidget()
            w.set_node(node)
            self.add_widget(w)
        self.update_layout()
        return partial(self.remove_nodes, nodes)
    @undoable_method
    def remove_nodes(self, nodes):
        self.set_status_text("Remove %d nodes" % (len(nodes),))
        for node in nodes:
            node.disconnect_all()
            self.remove_widget(node.value.widget)
        self.update_layout()
        return partial(self.add_nodes, nodes)

    @undoable_method
    def zoom(self, zoom):
        self.set_status_text("Zoom %d" % (zoom,))
        self.pos_zoom *= zoom
        self.size_zoom *= zoom
        self.update_layout()
        if zoom != 0:
            return partial(self.zoom, 1.0/zoom)

    #@undoable_method it's not so useful to undo this...
    def toggle_layout_engine(self, dirc):
        self.dot_prog_num = (self.dot_prog_num + dirc) % len(self.dot.layout_programs)
        prog = self.dot.layout_programs[self.dot_prog_num]
        self.set_status_text("Layout engine: %r" % (prog,))
        self.dot.set_process(prog)
        self.update_layout()
        #return partial(self.toggle_layout_engine, -dirc)
        
    def paint_connector(self, color, widgets):
        mpos = mouse_pos()
        for w in widgets:
            cpos = w.center_pos()
            paint_arrowhead_by_direction(self.screen, color, cpos, mpos)
            pygame.draw.aalines(self.screen, color, False,
                                [cpos.as_tuple(), mpos.as_tuple()], True)
        
    def paint_widgets(self, event):
        super(GraphApp, self).paint_widgets(event)
        if self.connecting:
            self.paint_connector((150,250,150), [n.value.widget for n in self.connecting_sources])
        if self.disconnecting:
            self.paint_connector((250,150,150), [n.value.widget for n in self.disconnecting_sources])
            
        self.paint_status_text()
        
        
    def _key_down(self, e):
        super(GraphApp, self)._key_down(e)
        if (e.mod & pygame.KMOD_CTRL):
            self.handle_control_key(e)
        else:
            if self.focused_widgets and len(self.focused_widgets) == 1:
                self.focused_widgets[0].node.value.entered_text(e)
                self.update_layout()

    def undo(self):
        self.set_status_text("Undo")
        if not self.history:
            return
        doer, undoer, args, kw = self.history.pop()
        self.undoing = True
        undoer()
        self.undoing = False

    def redo(self):
        self.set_status_text("Redo")
        if not self.history_redo:
            return
        doer, undoer, args, kw = self.history_redo.pop()
        self.undoing = False
        undoer()
        #self.undoing = False

    def toggle_record(self):
        if not self.record:
            self.start_record()
        else:
            self.stop_record()

    def create_new_node(self):
        self.add_nodes([Graph.Node(NodeValue('new'))])

    def delete_selected_nodes(self):
        if self.focused_widgets:
            self.remove_nodes([w.node for w in self.focused_widgets])
            self.unset_focus()

    def output_dot_description(self):
        nodes, groups = self._get_nodes_and_groups()
        print '\n'
        print Graph.generate_dot(groups)
        print '\n'

    def change_curve_resolution(self, amount_to_add):
        self.bezier_points += amount_to_add
        if self.bezier_points < 4:
            self.bezier_points = 4
        self.update_layout()

    def handle_control_key(self, e):
        if e.key in self.control_map:
            name, handler = self.control_map[e.key]
            handler()
            

    def _mouse_down(self, e):
        mods = pygame.key.get_mods()
        connect_modifier_used = (mods & pygame.KMOD_SHIFT)
        multiselect = (mods & self.multiselect_modifier)
        if not multiselect or (self.focused_widgets and self.hovered_widget not in self.focused_widgets):
            # The or part is to allow people to use a first click-drag
            # on the last widget of a multiselect group to
            # connect. Otherwise, the connection group would not
            # include that last widget.
            super(GraphApp, self)._mouse_down(e)
        if self.focused_widgets and connect_modifier_used:
            if e.button == 1:
                self.connecting = True
                self.connecting_sources = [w.node for w in self.focused_widgets]
            elif e.button == 3:
                self.disconnecting = True
                self.disconnecting_sources = [w.node for w in self.focused_widgets]
            self.unset_focus()
        if multiselect:
            super(GraphApp, self)._mouse_down(e)
            
                
    def _mouse_up(self, e):
        super(GraphApp, self)._mouse_up(e)
        if self.connecting:
            self.connecting = False
            target = self.hovered_widget
            if target:
                target = target.node
                self.connect_nodes(self.connecting_sources, target)
            self.connecting_source = None
        elif self.disconnecting:
            self.disconnecting = False
            target = self.hovered_widget
            if target:
                target = target.node
                self.disconnect_nodes(self.disconnecting_sources, target)
            self.disconnecting_source = None

    @undoable_method
    def connect_nodes(self, sources, target):
        self.set_status_text("Connect")
        for source in sources:
            source.connect(target)
            ew = source.value.widget.add_edge(target.value.widget)
            self.add_widget(ew)
        self.update_layout()
        return partial(self.disconnect_nodes, sources, target)
    
    @undoable_method
    def disconnect_nodes(self, sources, target):
        self.set_status_text("Disconnect")
        for source in sources:
            if source.is_connected(target):
                source.disconnect(target)
        self.update_layout()
        return partial(self.connect_nodes, sources, target)

    def _out_of_date(self, failure):
        failure.trap(OutOfDate)
        return None

    def iter_node_widgets(self):
        for widget in self.widgets:
            if isinstance(widget, NodeWidget):
                yield widget
                
    def _get_nodes_and_groups(self):
        nodes = [widget.node for widget in self.iter_node_widgets()]
        groups = {}
        for node in nodes:
            group_name = node.value.group_name
            groups.setdefault(group_name, []).append(node)
        return nodes, groups
        
    def update_layout(self):
        nodes, groups = self._get_nodes_and_groups()
        d = Graph.get_drawing_data(self.dot, groups)
        d.addCallbacks(self._layout, self._out_of_date)
        d.addErrback(twisted.python.log.err)

    def _layout(self, (g, n, e)):
        if not n:
            return
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
                    label = edge['label']
                    
                    from Lib.Bezier import Bezier
                    line.insert(0, (this.center_pos(False)))
                    line.append((other.center_pos(False)))
                    curve = Bezier(line, self.bezier_points)

                    connections = this.get_connection_lines_to(other)
                    # if there is more than one connection, we don't care to animate the correct one.
                    last_index = last_indices.setdefault(other, 0)
                    if len(connections) <= last_index:
                        ew = this.add_edge(other)
                        self.add_widget(ew)
                        
                    connections[last_index].line.final = curve
                    last_indices[other] += 1

                # IF we had MORE lines than now, remove the extra ones.
                for other, last_index in last_indices.iteritems():
                    connections = node.value.widget.out_connection_lines[other]
                    while len(connections) > last_index:
                        connections.pop(len(connections) - 1)
                    
            for other in previously_connected:
                del node.value.widget.out_connection_lines[other]

    def paint_status_text(self):
        new_list = []
        h = self.status_font.get_height() + 2
        for i, (timeout, rendered) in enumerate(self.rendered_status_texts[:]):
            if time.time() > timeout:
                continue
            new_list.append((timeout, rendered))
            self.screen.blit(rendered, (0,self.height-h*(i+1)))

        self.rendered_status_texts = new_list
        
    def set_status_text(self, text, timeout=6):
        if self.undoing:
            return
        for line in reversed(text.split('\n')):
            self.rendered_status_texts.append((time.time() + timeout, self.status_font.render(line, True, (255,100,100))))

    def show_help(self):
        for key, (name, func) in sorted(self.control_map.iteritems()):
            self.set_status_text('CTRL-%s - %s' % (pygame_reverse_key_map[key][len('K_'):], name), 15)
        
#---------------------------------------------


def test():
    pygame.init()
    a = GraphApp(800, 600)
    a.run()

if __name__=='__main__':
    test()
