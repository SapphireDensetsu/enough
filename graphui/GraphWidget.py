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

FILENAME = "graphui.data"

from functools import partial
import pygame
import time

import twisted.python.log

from App import AppWidget
from Widget import mouse_pos, Widget, undoable_method
from Lib import Graph
from Lib.Dot import Dot, OutOfDate
from Lib.Font import get_font, find_font
from Lib.Point import Point

from guilib import paint_arrowhead_by_direction, pygame_reverse_key_map

from scancodes import scancode_map

from graph_widgets import NodeWidget, EdgeWidget
from GraphElementValue import GraphElementValue

from RowWidget import make_row_menu

message = 'Graphui | http://code.google.com/p/enough | Enough Lame Computing! | GPLv3'

class GraphWidget(Widget):
    def __init__(self, *args, **kw):
        super(GraphWidget, self).__init__(*args, **kw)
        #pygame.display.set_caption('Graphui | Enough')
        self.dot = Dot()
        self.init_control_map()
        
        self.dragging_enabled = False
        self.connecting = False
        self.disconnecting = False
        self.preserve_aspect_ratio = True
        self.bezier_points = 30
        self.modal_nodes = None
        
        self.dot_prog_num = 0
        
        self.status_font = pygame.font.SysFont('serif',min(self.size.final.y/20, 18))
        self.rendered_status_texts = []
        self.set_status_text(message,15)
        self.set_status_text('CTRL-H for help', 15)

        self.pan_start_pos = None
        self.reset_zoom_pan()

        # TODO get rid of shape in Widget (move it to some ShapeWidget or whatever)
        #self.shape = None
        #self.params.fore_color = None
        self.params.back_color = None
        self.params.focus_back_color = None
        self.params.hover_back_color = None
        self.params.focus_fore_color = (150,150,255)

        self._last_group = 0
        
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
                            pygame.K_i: ("Save snapshot image", partial(self.save_snapshot_image, "graphui.snapshot.bmp")),
                            pygame.K_a: ("Create new node", self.create_new_node),
                            pygame.K_o: ("Output DOT description", self.output_dot_description),
                            pygame.K_EQUALS: ("Higher curve resolution", partial(self.change_curve_resolution,
                                                                                 3)),
                            pygame.K_MINUS: ("Lower curve resolution", partial(self.change_curve_resolution,
                                                                               -3)),
                            pygame.K_h: ("Show help", self.show_help),
                            pygame.K_F1:("Show help", self.show_help),
                            pygame.K_k: ("Switch layout engine", partial(self.toggle_layout_engine, 1)),
                            pygame.K_d: ("Delete selected node/edge", self.delete_focused),
                            pygame.K_1: ("Smaller font for node/edge", partial(self.focused_font_size, 1/1.1)),
                            pygame.K_2: ("Larger font for node/edge", partial(self.focused_font_size, 1.1)),
                            
                            pygame.K_e: ("Toggle stretch/keep aspect ratio", self.toggle_aspect_ratio),
                            pygame.K_r: ("Reset zoom & pan", self.reset_zoom_pan),
                            
                            pygame.K_s: ("Save", self.save),
                            pygame.K_l: ("Load", self.load),

                            pygame.K_g: ("Group selected nodes", self.assign_to_group),
                            pygame.K_f: ("Ungroup selected nodes", self.unassign_to_group),
                            pygame.K_b: ("Toggle showing group names", self.toggle_show_group_names),
                            }
    @undoable_method
    def add_nodes(self, nodes):
        self.set_status_text("Add %d nodes" % (len(nodes),))
        for node in nodes:
            w = NodeWidget(start_pos=self.size.current*0.5)
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
        if self.focused_widgets is None:
            return
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
        
    def paint_connector(self, parent_offset, surface, color, widgets):
        mpos = mouse_pos()
        for w in widgets:
            cpos = w.center_pos() + self.pos.current + parent_offset
            paint_arrowhead_by_direction(surface, color, cpos, mpos)
            pygame.draw.aalines(surface, color, False,
                                [tuple(cpos), tuple(mpos)], True)
        
    def paint_widgets(self, event):
        super(GraphWidget, self).paint_widgets(event)
        surface = event.surface
        if self.connecting:
            self.paint_connector(event.parent_offset, surface, (150,250,150), [n.value.widget for n in self.connecting_sources])
        if self.disconnecting:
            self.paint_connector(event.parent_offset, surface, (250,150,150), [n.value.widget for n in self.disconnecting_sources])
        self.paint_status_text(event.parent_offset, event.surface)
            
        
    def key_down(self, when, event):
        super(GraphWidget, self).key_down(when, event)
        if when == 'post':
            return False
        
        e = event.pygame_event
        if (e.mod & pygame.KMOD_CTRL):
            self.handle_control_key(e)
            return True
        else:
            return False

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

    def _connect_modifier_used(self, mods=None):
        return self._modkey_used(pygame.KMOD_SHIFT)
    def _pan_modifier_used(self, mods=None):
        #return self._modkey_used(pygame.KMOD_ALT)
        b1, b2, b3 = pygame.mouse.get_pressed()
        return b1 & b3
        
    def mouse_down(self, when, event):
        res = super(GraphWidget, self).mouse_down(when, event)
        if res == 'pre':
            return res
        
        e = event.pygame_event
        mods = pygame.key.get_mods()
        if self._pan_modifier_used(mods):
            self.pan_start_offset = self.pan_offset
            self.pan_start_pos = mouse_pos() 
            return True
            
        multiselect = self._multiselect_modifier_used(mods)
        if self.focused_widgets and self._connect_modifier_used(mods):
            if e.button == 1:
                self.connecting = True
                self.connecting_sources = [w.node for w in self.focused_widgets if isinstance(w, NodeWidget)]
            elif e.button == 3:
                self.disconnecting = True
                self.disconnecting_sources = [w.node for w in self.focused_widgets if isinstance(w, NodeWidget)]
            self.unset_focus()
        return True
            
    def mouse_motion(self, when, event):
        res = super(GraphWidget, self).mouse_motion(when, event)
        if when == 'post':
            return res

        e = event.pygame_event
        if self._pan_modifier_used():
            p = mouse_pos()
            self.pan_offset = p - self.pan_start_pos + self.pan_start_offset
            self.update_layout()
        return False
            
                
    def mouse_up(self, when, event):
        res = super(GraphWidget, self).mouse_up(when, event)
        if when == 'post':
            return res
        
        e = event.pygame_event
        if self._pan_modifier_used():
            self.update_layout()
            return False
        
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
            
        elif e.button == 3:
            # right click
            menu = make_row_menu((('transpose',None),('test',None),('this',None)), self.chosen)
            menu.params.in_drag_mode = True
            menu.painting_z_order = NodeWidget.painting_z_order + 1
            menu.transpose()
            self.add_widget(menu)
            
        else:
            return False

        return True

    def chosen(self, menu, (label,value), clicked_widget, event):
        if label=='transpose':
            menu.transpose()
            return
        if not clicked_widget.in_bounds(event.pos + clicked_widget.pos.current):
            return
        print label, value
        self.remove_widget(menu)
    
    def _add_edge(self, source, target, label='edge'):
        edge = Graph.Edge(source, target, GraphElementValue(label))
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
                
    def assign_to_group(self):
        self._last_group += 1
        for widget in self.focused_widgets:
            if isinstance(widget, NodeWidget):
                widget.node.value.group_name = str(self._last_group)
        self.update_layout()

    def unassign_to_group(self):
        for widget in self.focused_widgets:
            if isinstance(widget, NodeWidget):
                widget.node.value.group_name = None
        self.update_layout()

    def toggle_show_group_names(self):
        for widget in self.widgets:
            if isinstance(widget, NodeWidget):
                widget.params.show_group_name = not widget.params.show_group_name
        self.update_layout()
        
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
        x_scale = self.size.final.x / g_width * self.pos_zoom
        y_scale = self.size.final.y / g_height * self.pos_zoom
        x_offset = self.pan_offset.x
        y_offset = self.pan_offset.y
        if self.preserve_aspect_ratio:
            x_scale = y_scale = min(x_scale, y_scale)
            x_offset += (self.size.final.x - (x_scale * g_width)) / 2
            y_offset += (self.size.final.y - (y_scale * g_height)) / 2
        
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

    def paint_status_text(self, parent_offset, surface):
        new_list = []
        h = self.status_font.get_height() + 2
        for i, (timeout, rendered) in enumerate(self.rendered_status_texts[:]):
            if time.time() > timeout:
                continue
            new_list.append((timeout, rendered))
            surface.blit(rendered, (0,self.size.current.y-h*(i+1)+self.pos.current.y+parent_offset.y))

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

    EXT='.bmp' # until we get support for jpg/png/gif whatever
    def save(self):
        # TODO fix the image code its ugly
        filename = FILENAME
        ext=self.EXT
        try:
            def done_snapshot(filename_ext, width, height):
                image = open(filename+ext, 'rb').read()
                self.set_status_text("Saving to %r..." % (filename,), 2)
                super(GraphWidget, self).save(filename+'.tmp')
                saved = open(filename+'.tmp', 'rb').read()
                import struct
                image_size = struct.pack('L', len(image))
                open(filename+ext, 'wb').write(image + saved + image_size)
                
            self.save_snapshot_on_next_paint(filename+ext, callback_when_done=done_snapshot)
            
        except Exception, e:
            self.set_status_text("Save failed %s" % (e,))
            return
        self.set_status_text("Saved successfully")
        

    def load(self):
        filename = FILENAME
        ext=self.EXT
        try:
            f=open(filename+ext, 'rb')
            f.seek(-4,2)
            import struct
            image_len, = struct.unpack('L', f.read())
            f.seek(image_len)
            saved = f.read()[:-4]
            open(filename+'.tmp', 'wb').write(saved)
            self.set_status_text("Loading from %s..." % (filename,), 2)
            super(GraphWidget, self).load(filename+'.tmp')
        except Exception, e:
            self.set_status_text("Load failed %s" % (e,))
            raise
        self.update_layout()

    def save_snapshot_image(self, event, filename, *args, **kw):
        self.set_status_text("Saving snapshot to %r" % (filename,), 5)
        # We don't want the status text to appear in the snaphot
        t = self.rendered_status_texts
        self.rendered_status_texts = []
        self.set_status_text("This is a Graphui file", 9999)
        self.set_status_text("Do NOT edit in imaging programs, use Graphui!", 9999)
        # TODO : There is some bug here, the widgets are not painted in the correct order?
        #self.cause_paint()
        if not kw['width'] and not kw['height']:
            kw['width'] = 640
        super(GraphWidget, self).save_snapshot_image(event, filename, *args, **kw)
        
        self.rendered_status_texts = t


