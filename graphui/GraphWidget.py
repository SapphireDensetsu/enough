# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from Lib.Func import PicklablePartial as partial

import pygame
import draw
from guilib import MovingValue, MovingLine
from Lib.Point import Point
from Widget import Widget
from NodeWidget import NodeWidget
from EdgeWidget import EdgeWidget

from Lib import observer

from Keymap import Keymap, Key

from Lib.observable.SortedItems import SortedItems
from Lib.observable.Dict import Dict

from Lib import Graph

from layout import Layout

import loop

class GraphWidget(Widget):
    bg_color=(0,0,0)
    activated_bg_color=(10,10,20)

    key_create_node = Key(pygame.KMOD_CTRL, pygame.K_a)
    key_delete_node = Key(pygame.KMOD_CTRL, pygame.K_d)
    key_next_node = Key(0, pygame.K_TAB)
    key_prev_node = Key(pygame.KMOD_SHIFT, pygame.K_TAB)
    key_select_node_right = Key(0, pygame.K_RIGHT)
    key_select_node_left = Key(0, pygame.K_LEFT)
    key_select_node_up = Key(0, pygame.K_UP)
    key_select_node_down = Key(0, pygame.K_DOWN)
    key_connect = Key(pygame.KMOD_CTRL, pygame.K_RETURN)
    key_cycle_layout = Key(pygame.KMOD_CTRL, pygame.K_k)
    #key_export_dot = Key(pygame.KMOD_CTRL, pygame.K_)
    key_export_snapshot = Key(pygame.KMOD_CTRL, pygame.K_x)

    key_save = Key(pygame.KMOD_CTRL, pygame.K_s)
    key_load = Key(pygame.KMOD_CTRL, pygame.K_l)
    
    def __init__(self, size, *args, **kw):
        Widget.__init__(self, *args, **kw)
        self._size = MovingValue(Point, final=Point(size))
        self.nodes = set()
        self.edges = set()
        self.node_widgets = Dict()
        self.edge_widgets = Dict()
        self.sorted_widgets = SortedItems(self.node_widgets)

        self.layout = Layout()
        
        self.selected_widget_index = None
        self._update_index()

        self._connector_start_pos = None
        self._connect_source_node = None

        self._register_keys()
        self._save_next_display_update = False
        
    def __getstate__(self):
        d= self.__dict__.copy()
        del d['parenting_keymap']
        del d['focus_keymap']
        del d['keymap']
        return d
    def __setstate__(self, d):
        for k,v in d.iteritems():
            self.__dict__[k] = v
        self.focus_keymap = Keymap()
        self.keymap = Keymap()
        self._register_keys()

    def _register_keys(self):
        self.parenting_keymap = Keymap()
        r = self.keymap.register_key_noarg
        r(self.key_create_node, self._create_new_node)
        r(self.key_connect, self._start_connect)
        r(self.key_cycle_layout, self._cycle_layout_engine)
        r(self.key_save, self._save)
        r(self.key_load, self._load)
        r(self.key_export_snapshot, self._export_snapshot)
        self._set_next_keymap()

    def get_size(self):
        return self._size.current
    def set_size(self, p):
        self._size.final = p 
    size = property(get_size, set_size)
    
    def _node_connect(self, e):
        for node in e.source, e.target:
            if node not in self.nodes:
                self.add_node(node)
        if e not in self.edges:
            self.add_edge(e)
    def _node_disconnect(self, e):
        self.remove_edge(e)

    def update_edges_lines(self, widget, node):
        center = Point(widget.final_rect().center)
        for edge in node.connections['in']:
            edge_w = self.edge_widgets[edge]
            edge_w.line.final[-1] = center.copy()
            edge_w.line.reset()
        for edge in node.connections['out']:
            edge_w = self.edge_widgets[edge]
            edge_w.line.final[0] = center.copy()
            edge_w.line.reset()
        
    def _node_widget_loc_pos_set(self, widget, node, new_pos):
        self.update_edges_lines(widget, node)
    def _node_widget_loc_size_set(self, widget, node, new_size):
        self.update_edges_lines(widget, node)
        
    def add_edge(self, edge):
        edge.obs.add_observer(self, '_edge_')
        self.edges.add(edge)
        if edge.source in self.node_widgets:
            source = self.node_widgets[edge.source].final_rect().center
        if edge.target in self.node_widgets:
            target = self.node_widgets[edge.target].final_rect().center
        w = EdgeWidget(edge, partial(self.node_widgets.get),
                       MovingLine(list, [Point(source), Point(target)]))
        self.edge_widgets[edge] = w
        self.update_layout()
    def remove_edge(self, edge):
        edge.obs.remove_observer(self)
        del self.edge_widgets[edge]
        self.edges.remove(edge)
        self.update_layout()

    def add_node(self, node):
        self.nodes.add(node)
        w = NodeWidget(node)
        self.node_widgets[node] = w
        node.obs.add_observer(self, '_node_')
        w.obs_loc.add_observer(self, '_node_widget_loc_', w, node)
        self.update_layout()
        loop.loop.mouse_map.push_area(w.mouse_area, partial(self._widget_mouse_event, node, w))
        return w
    def remove_node(self, node):
        w = self.node_widgets[node]
        w.obs_loc.remove_observer(self)
        node.obs.remove_observer(self)
        del self.node_widgets[node]
        self.nodes.remove(node)
        self._update_index()
        self.update_layout()
        return w

    def generate_groups(self):
        groups = {'0':[]}
        for node in self.nodes:
            groups['0'].append(node)
        return groups

    def update_layout(self):
        groups = self.generate_groups()
        self.layout.update(groups, self.size, self.node_widgets, self.edge_widgets)
        
    def update(self):
        if self.node_widgets:
            #  Todo rewrite this highly-unoptimized code!
            font_size_average = 0
            font_sizes = {}
            dists = {}
            for w in self.node_widgets.itervalues():
                size = w.reset_max_text_size()
                font_size_average += size
                font_sizes[w] = size
            font_size_average /= len(self.node_widgets)
            variance = 0
            for w in self.node_widgets.itervalues():
                size = font_sizes[w]
                dist = (size - font_size_average)**2
                dists[w] = dist
                variance += dist
            variance /= len(self.node_widgets)
            for w in self.node_widgets.itervalues():
                if variance != 0:
                    size = font_sizes[w]
                    dist = dists[w]
                    if  dist / variance > 0.3:
                        if size > font_size_average:
                            w._update_text_size(font_size_average)
                w.update()
        for w in self.edge_widgets.itervalues():
            w.update()
        self._size.update()
        
        
    def _draw(self, surface, pos):
        for w in self.edge_widgets.values():
            p = Point(pos)
            w._draw(surface, pos)
        for w in self.node_widgets.values():
            # for our children, pos is the parent's pos offset
            # because of how NodeWidget works.
            w._draw(surface, pos)

        if self._connector_start_pos is not None:
            n,w = self.selected()
            if w is not None:
                start_pos = self._connector_start_pos()
                end_pos = self._connector_end_pos()
                draw.line(surface, (50,255,50), start_pos, end_pos)

        if self._save_next_display_update:
            draw.save(surface, self._save_next_display_update)
            self._save_next_display_update = None

    def selected(self):
        if self.selected_widget_index is None:
            return None, None
        return self.sorted_widgets[self.selected_widget_index]
    
    def _set_next_keymap(self):
        self.keymap.set_next_keymap(self.parenting_keymap)
        if self.selected_widget_index is not None:
            self.parenting_keymap.set_next_keymap(self.selected()[1].keymap)
            r = self.parenting_keymap.register_key_noarg
            r(self.key_delete_node, self._delete_selected_node)
            r(self.key_next_node, self._next_node)
            r(self.key_prev_node, self._prev_node)
            r(self.key_select_node_right, self._select_node_right)
            r(self.key_select_node_left, self._select_node_left)
            r(self.key_select_node_up, self._select_node_up)
            r(self.key_select_node_down, self._select_node_down)
        else:
            ur = self.parenting_keymap.unregister_key
            ur(self.key_next_node)
            ur(self.key_prev_node)
            ur(self.key_select_node_right)
            ur(self.key_select_node_left)
            ur(self.key_select_node_up)
            ur(self.key_select_node_down)
            ur(self.key_delete_node)
            self.parenting_keymap.set_next_keymap(self.focus_keymap)
    
    def _set_index(self, index):
        if self.selected_widget_index != index:
            self.selected_widget_index = index
        self._update_index()

    def _update_index(self):
        if not self.node_widgets:
            self.selected_widget_index = None
        else:
            self.selected_widget_index %= len(self.sorted_widgets)
            self._set_next_keymap()
            
    def _find_widget_index(self, w):
        for i, (node, widget) in enumerate(self.sorted_widgets):
            if w == widget:
                return i
            
    def _add_index(self, amount):
        if self.selected_widget_index is None:
            index = 0
        else:
            index = self.selected_widget_index
            l = len(self.sorted_widgets)
            index += amount
            index %= l
        self._set_index(index)


    def _next_node(self):
        '''Next node'''
        self._add_index(1)
    def _prev_node(self):
        '''Previous node'''
        self._add_index(-1)

    def _select_node_right(self):
        '''Select the next node to the right'''
        def dist(pos1, pos2):
            if pos1.x < pos2.x:
                return None
            return pos1.x - pos2.x
        self._select_node_dir(dist)
        
    def _select_node_left(self):
        '''Select the next node to the left'''
        def dist(pos1, pos2):
            if pos1.x > pos2.x:
                return None
            return pos2.x - pos1.x
        self._select_node_dir(dist)

    def _select_node_up(self):
        '''Select the next node above'''
        def dist(pos1, pos2):
            if pos1.y > pos2.y:
                return None
            return pos2.y - pos1.y
        self._select_node_dir(dist)

    def _select_node_down(self):
        '''Select the next node below'''
        def dist(pos1, pos2):
            if pos1.y < pos2.y:
                return None
            return pos1.y - pos2.y
        self._select_node_dir(dist)

    def _select_node_dir(self, distance_between):
        closest_right = None
        min_dist = None
        n, w = self.selected()
        if not w:
            return
        for widget in self.node_widgets.itervalues():
            if widget == w:
                continue
            dist = distance_between(widget.pos, w.pos)
            if dist is None:
                continue
            if closest_right is None or dist < min_dist:
                closest_right = widget
                min_dist = dist
                
        if closest_right is not None:
            i = self._find_widget_index(closest_right)
            self._set_index(i)
            
    def _create_new_node(self):
        '''Create new node'''
        n = Graph.Node()
        w = self.add_node(n)
        self._set_index(self._find_widget_index(w))
        
    def _delete_selected_node(self):
        '''Delete selected node'''
        n, w = self.sorted_widgets[self.selected_widget_index]
        n.disconnect_all()
        self._add_index(1)
        self.remove_node(n)

    def _node_connection_started(self):
        r = self.keymap.register_key_noarg
        ur = self.keymap.unregister_key
        start_node, start_node_widget = self.selected()
        assert start_node is not None
        def _end_connect():
            '''Sets the target node to connect'''
            ur(self.key_connect)
            r(self.key_connect, self._start_connect)

            end_node, end_node_widget = self.sorted_widgets[self.selected_widget_index]
            start_node.connect_node(end_node)
            self._connector_start_pos = None
            self._connector_end_pos = None

        def _end_pos():
            n, w = self.selected()
            if w is None:
                return None
            return w.rect().center
            
        ur(self.key_connect)
        r(self.key_connect, _end_connect)
        self._connector_start_pos = lambda : start_node_widget.rect().center
        self._connector_end_pos = _end_pos
        
    def _start_connect(self):
        '''Sets the source node to connect'''
        self._node_connection_started()

    def _widget_mouse_event(self, node, widget, event):
        connect_mod = pygame.key.get_mods() & pygame.KMOD_SHIFT
        if event.type == pygame.MOUSEBUTTONDOWN:
            i = self._find_widget_index(widget)
            self._set_index(i)
            if connect_mod and self._connector_start_pos is None:
                self._connect_source_node = node
                self._connector_start_pos = lambda : widget.rect().center
                self._connector_end_pos = pygame.mouse.get_pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if self._connector_start_pos is not None:
                self._connector_start_pos = None
                self._connector_end_pos = None
                self._connect_source_node.connect_node(node)
                self._connect_source_node = None
                
        
    def _cycle_layout_engine(self):
        '''Change to the next layout engine'''
        self.layout.cycle_layout_engines()
        self.update_layout()

    def _save(self):
        '''Save'''
        import pickle
        f=open('save.pkl', 'wb')
        pickle.dump(self,f,2)

    def _load(self):
        '''Load'''
        import pickle
        f=open('save.pkl', 'rb')
        newself = pickle.load(f)
        loop.loop.browser.main_stack.pop()
        loop.loop.browser.main_stack.push(newself)

    def _export_dot(self):
        '''Export the graph to a .dot file'''
        d = Graph.generate_dot(self.generate_groups())
        print d
        open('save.dot', 'wb').write(d)

    def _export_snapshot(self):
        '''Export the graph to a snapshot image'''
        self._save_next_display_update = 'snapshot.bmp'
