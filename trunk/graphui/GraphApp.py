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

from functools import partial
import pygame
import time

import twisted.python.log

from App import App, mouse_pos, undoable_method
from Lib import Graph
from Lib.Dot import Dot, OutOfDate
from Lib.Font import get_font, find_font
from Lib.Point import Point

from guilib import paint_arrowhead_by_direction, pygame_reverse_key_map

from scancodes import scancode_map

from graph_widgets import NodeWidget, EdgeWidget
from GraphElementValue import GraphElementValue


message = 'Graphui | http://code.google.com/p/enough | Enough Lame Computing! | GPLv3'

class GraphApp(App):
    def __init__(self, *args, **kw):
        super(GraphApp, self).__init__(*args, **kw)
        pygame.display.set_caption('Graphui | Enough')
        self.dot = Dot()
        self.init_control_map()
        
        self.dragging_enabled = False
        self.connecting = False
        self.disconnecting = False
        self.preserve_aspect_ratio = True
        self.bezier_points = 30
        self.modal_nodes = None
        
        self.dot_prog_num = 0
        
        self.status_font = pygame.font.SysFont('serif',min(self.height/20, 18))
        self.rendered_status_texts = []
        self.set_status_text(message,15)
        self.set_status_text('CTRL-H for help', 15)

        self.pan_start_pos = None
        self.reset_zoom_pan()

    def reset_zoom_pan(self):
        self.pan_offset = Point((0,0))
        self.pos_zoom = 1
        self.size_zoom = 0.8
        self.update_layout()
        
    def init_control_map(self):
        zoom_amount = 1.3
        self.control_map = {pygame.K_w: ("Zoom in", partial(self.zoom, zoom_amount)),
                            pygame.K_q: ("Zoom out", partial(self.zoom, 1.0/zoom_amount)),
                            pygame.K_z: ("Undo", self.undo),
                            pygame.K_y: ("Redo", self.redo),
                            pygame.K_p: ("Record (toggle)", self.toggle_record),
                            pygame.K_a: ("Create new node", self.create_new_node),
                            pygame.K_s: ("Output DOT description", self.output_dot_description),
                            pygame.K_EQUALS: ("Higher curve resolution", partial(self.change_curve_resolution,
                                                                                 3)),
                            pygame.K_MINUS: ("Lower curve resolution", partial(self.change_curve_resolution,
                                                                               -3)),
                            pygame.K_h: ("Show help", self.show_help),
                            pygame.K_F1:("Show help", self.show_help),
                            pygame.K_l: ("Switch layout engine", partial(self.toggle_layout_engine, 1)),
                            pygame.K_d: ("Delete selected node/edge", self.delete_focused),
                            pygame.K_1: ("Smaller font for node/edge", partial(self.focused_font_size, 1/1.1)),
                            pygame.K_2: ("Larger font for node/edge", partial(self.focused_font_size, 1.1)),
                            
                            pygame.K_e: ("Toggle stretch/keep aspect ratio", self.toggle_aspect_ratio),
                            pygame.K_r: ("Reset zoom & pan", self.reset_zoom_pan),
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
            removed_edges = node.disconnect_all()
            for edge in removed_edges:
                # The edge itself has been removed from the graph
                # already, remove only the widget
                self._remove_edge_widget_of_edge(edge)
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

    def delete_focused(self):
        nodes = []
        for w in self.focused_widgets:
            if isinstance(w, NodeWidget):
                nodes.append(w.node)
            elif isinstance(w, EdgeWidget):
                self._remove_edge(w.edge)
        if nodes:
            self.remove_nodes(nodes)
        self.unset_focus()
        self.update_layout()

            
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
                                [tuple(cpos), tuple(mpos)], True)
        
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
                widget, = self.focused_widgets
                widget.entered_text(e)
                self.update_layout()

    def toggle_record(self):
        if not self.record:
            self.start_record()
        else:
            self.stop_record()

    def create_new_node(self):
        self.add_nodes([Graph.Node(GraphElementValue('new'))])

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
        scancode = getattr(e, 'scancode', None)

        key = e.key
        if scancode is not None:
            if scancode not in scancode_map:
                print 'Unknown scancode', scancode, 'key=', e.key, 'unicode=', e.unicode
            key = scancode_map.get(scancode, e.key)
        if key in self.control_map:
            name, handler = self.control_map[key]
            handler()

    def _modkey_used(self, key, mods=None):
        if not mods:
            mods = pygame.key.get_mods()
        return mods & key
    def _connect_modifier_used(self, mods=None):
        return self._modkey_used(pygame.KMOD_SHIFT)
    def _multiselect_modifier_used(self, mods=None):
        return self._modkey_used(self.multiselect_modifier)
    def _pan_modifier_used(self, mods=None):
        #return self._modkey_used(pygame.KMOD_ALT)
        b1, b2, b3 = pygame.mouse.get_pressed()
        return b1 & b3
        
    def _mouse_down(self, e):
        mods = pygame.key.get_mods()
        if self._pan_modifier_used(mods):
            self.pan_start_offset = self.pan_offset
            self.pan_start_pos = mouse_pos() 
            return
            
        multiselect = self._multiselect_modifier_used(mods)
        if (not multiselect
            or (self.focused_widgets and self.hovered_widget not in self.focused_widgets)):
            # The or part is to allow people to use a first click-drag
            # on the last widget of a multiselect group to
            # connect. Otherwise, the connection group would not
            # include that last widget.
            super(GraphApp, self)._mouse_down(e)
        if self.focused_widgets and self._connect_modifier_used(mods):
            if e.button == 1:
                self.connecting = True
                self.connecting_sources = [w.node for w in self.focused_widgets if isinstance(w, NodeWidget)]
            elif e.button == 3:
                self.disconnecting = True
                self.disconnecting_sources = [w.node for w in self.focused_widgets if isinstance(w, NodeWidget)]
            self.unset_focus()
        if multiselect:
            super(GraphApp, self)._mouse_down(e)
            
    def _mouse_motion(self, e):
        super(GraphApp, self)._mouse_motion(e)
        if self._pan_modifier_used():
            p = mouse_pos()
            self.pan_offset = p - self.pan_start_pos + self.pan_start_offset
            self.update_layout()
            
                
    def _mouse_up(self, e):
        super(GraphApp, self)._mouse_up(e)
        if self._pan_modifier_used():
            self.update_layout()
            return
        
        if self.connecting:
            self.connecting = False
            target = self.hovered_widget
            if isinstance(target, NodeWidget):
                target = target.node
                self.connect_nodes(self.connecting_sources, target)
            self.connecting_source = None
        elif self.disconnecting:
            self.disconnecting = False
            target = self.hovered_widget
            if isinstance(target, NodeWidget):
                target = target.node
                self.disconnect_nodes(self.disconnecting_sources, target)
            self.disconnecting_source = None

    def _add_edge(self, source, target):
        edge = Graph.Edge(source, target, GraphElementValue("edge"))
        source.connect_edge(edge)
        edge_widget = source.value.widget.add_edge(edge)
        edge.value.set_widget(edge_widget)
        self.add_widget(edge_widget)
        
    @undoable_method
    def connect_nodes(self, sources, target):
        self.set_status_text("Connect")
        for source in sources:
            self._add_edge(source, target)
        self.update_layout()
        return partial(self.disconnect_nodes, sources, target)

    def _remove_edge_widget_of_edge(self, edge):
        ew = edge.value.widget
        self.remove_widget(ew)
        edge.source.value.widget.remove_edge(ew)

    def _remove_edge(self, edge):
        self._remove_edge_widget_of_edge(edge)
        edge.source.disconnect_edge(edge)
        
    @undoable_method
    def disconnect_nodes(self, sources, target):
        self.set_status_text("Disconnect")
        for source in sources:
            if source.is_connected_node(target):
                for edge in source.edges_connected_to(target):
                    self._remove_edge(edge)
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
        g_height, g_width = float(g['height']), float(g['width'])
        x_scale = self.width / g_width * self.pos_zoom
        y_scale = self.height / g_height * self.pos_zoom
        x_offset = self.pan_offset.x
        y_offset = self.pan_offset.y
        if self.preserve_aspect_ratio:
            x_scale = y_scale = min(x_scale, y_scale)
            x_offset += (self.width - (x_scale * g_width)) / 2
            y_offset += (self.height - (y_scale * g_height)) / 2
        
        for node, n_layout in n.iteritems():
            node.value.widget.pos.final.x = n_layout['x'] * x_scale + x_offset
            node.value.widget.pos.final.y = n_layout['y'] * y_scale + y_offset
            node.value.widget.size.final.x = n_layout['width'] * x_scale * self.size_zoom
            node.value.widget.size.final.y = n_layout['height'] * y_scale * self.size_zoom
            node.value.widget.pos.final = node.value.widget.pos.final - node.value.widget.size.final * 0.5 
            node.value.widget.pos.reset()
            node.value.widget.size.reset()

        for node, n_layout in n.iteritems():
            lines = []
            if node in e:
                last_indices = {}
                for edge, dot_edge in e[node].iteritems():
                    edge.value.widget.update_from_dot(dot_edge,
                                                      x_scale=x_scale, y_scale=y_scale, x_offset=x_offset, y_offset=y_offset,
                                                      bezier_points=self.bezier_points)

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
        self.set_status_text(message, 10)
        for key, (name, func) in sorted(self.control_map.iteritems()):
            self.set_status_text('CTRL-%s - %s' % (pygame_reverse_key_map[key][len('K_'):], name), 10)

    def focused_font_size(self, dir):
        if not self.focused_widgets:
            return
        for w in self.focused_widgets:
            w.change_font_size(mul=dir)
        self.update_layout()

    def toggle_aspect_ratio(self):
        self.preserve_aspect_ratio = not self.preserve_aspect_ratio
        self.update_layout()
