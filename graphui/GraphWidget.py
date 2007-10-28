# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from lib.FuncTools import PicklablePartial as partial

import pygame
from gui import draw
from guilib import MovingValue, MovingLine
from Lib.Point import Point
from gui.Widget import Widget
from NodeWidget import NodeWidget
from EdgeWidget import EdgeWidget

from lib import observer

from gui.Keymap import Keymap, Key,keydown_noarg

from lib.observable.SortedItems import SortedItems
from lib.observable.Dict import Dict

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
        d = Widget.__getstate__(self)
        del d['parenting_keymap']
        return d
    def __setstate__(self, d):
        Widget.__setstate__(self, d)
        self._register_keys()

    def _register_keys(self):
        self.parenting_keymap = Keymap()
        r = self.keymap.register_key
        r(self.key_create_node, keydown_noarg(self._create_new_node))
        r(self.key_cycle_layout, keydown_noarg(self._cycle_layout_engine))
        r(self.key_save, keydown_noarg(self._save))
        r(self.key_load, keydown_noarg(self._load))
        r(self.key_export_snapshot, keydown_noarg(self._export_snapshot))
        self._set_next_keymap()

    def get_size(self):
        return tuple(self._size.current)
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
        if node in self.nodes:
            return
        self.nodes.add(node)
        w = NodeWidget(node)
        self.node_widgets[node] = w
        node.obs.add_observer(self, '_node_')
        w.obs_loc.add_observer(self, '_node_widget_loc_', w, node)
        self.update_layout()
        loop.loop.mouse_map.push_area(w.mouse_area, partial(self._widget_mouse_event, node, w))
        # They might be adding a node that is connected to some other,
        # yet-to-be added nodes
        for edge in node.iter_all_connections():
            self.add_edge(edge)
        return w
    def remove_node(self, node):
        node.disconnect_all()
        w = self.node_widgets[node]
        loop.loop.mouse_map.remove_area(w.mouse_area)
        w.obs_loc.remove_observer(self)
        node.obs.remove_observer(self)
        del self.node_widgets[node]
        self.nodes.remove(node)
        self._update_index()
        self.update_layout()
        if self._connect_source_node:
            self._connect_source_node = None
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
##             import math
##             # todo rewrite this shitty code
##             sizes = {}
##             slots = {}
##             slots_size = {}
##             slot_places = {}
##             average = 0
##             num = len(self.node_widgets)
##             for w in self.node_widgets.values():
##                 size = w.reset_max_text_size()
##                 sizes[w] = size
##             for w, size in sizes.iteritems():
##                 dist = int(round(math.log(size + 1)))
##                 slot = dist 
##                 slots.setdefault(slot, 0)
##                 slots_size.setdefault(slot, 0)
                
##                 slot_places[w] = slot
##                 slots[slot] += size
##                 slots_size[slot] += 1

##             for slot in slots:
##                 if slot in slots_size:
##                     num = slots_size[slot]
##                     if num > 0:
##                         slots[slot] /= slots_size[slot]
##             for w,slot in slot_places.iteritems():
##                 size = sizes[w]
##                 new_max_size = slots[slot]
##                 if new_max_size < size:
##                     w.reset_max_text_size(new_max_size)
            for w in self.node_widgets.values():
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
            r = self.parenting_keymap.register_key
            r(self.key_delete_node, keydown_noarg(self._delete_selected_node))
            r(self.key_next_node, keydown_noarg(self._next_node))
            r(self.key_prev_node, keydown_noarg(self._prev_node))
            r(self.key_select_node_right, keydown_noarg(self._select_node_right))
            r(self.key_select_node_left, keydown_noarg(self._select_node_left))
            r(self.key_select_node_up, keydown_noarg(self._select_node_up))
            r(self.key_select_node_down, keydown_noarg(self._select_node_down))
            if self.key_connect not in self.parenting_keymap:
                r(self.key_connect, keydown_noarg(self._start_connect))
        else:
            ur = self.parenting_keymap.unregister_key
            ur(self.key_next_node)
            ur(self.key_prev_node)
            ur(self.key_select_node_right)
            ur(self.key_select_node_left)
            ur(self.key_select_node_up)
            ur(self.key_select_node_down)
            ur(self.key_delete_node)
            ur(self.key_connect)
            self.parenting_keymap.set_next_keymap(self.focus_keymap)
    
    def _set_index(self, index):
        if self.selected_widget_index != index:
            self.selected_widget_index = index
        self._update_index()

    def _update_index(self):
        if not self.node_widgets:
            self.selected_widget_index = None
        elif self.selected_widget_index is not None:
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
            if pos1[0] < pos2[0]:
                return None
            return pos1[0] - pos2[0]
        self._select_node_dir(dist)
        
    def _select_node_left(self):
        '''Select the next node to the left'''
        def dist(pos1, pos2):
            if pos1[0] > pos2[1]:
                return None
            return pos2[0] - pos1[0]
        self._select_node_dir(dist)

    def _select_node_up(self):
        '''Select the next node above'''
        def dist(pos1, pos2):
            if pos1[1] > pos2[1]:
                return None
            return pos2[1] - pos1[1]
        self._select_node_dir(dist)

    def _select_node_down(self):
        '''Select the next node below'''
        def dist(pos1, pos2):
            if pos1[1] < pos2[1]:
                return None
            return pos1[1] - pos2[1]
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
        self._add_index(1)
        self.remove_node(n)

    def _node_connection_started(self):
        r = self.parenting_keymap.register_key
        ur = self.parenting_keymap.unregister_key
        start_node, start_node_widget = self.selected()
        assert start_node is not None
        def _end_connect():
            '''Sets the target node to connect'''
            ur(self.key_connect)
            r(self.key_connect, keydown_noarg(self._start_connect))

            end_node, end_node_widget = self.sorted_widgets[self.selected_widget_index]
            start_node.connect_node(end_node)
            self._connector_start_pos = None
            self._connector_end_pos = None

        def _start_pos():
            return start_node_widget.rect().center
        def _end_pos():
            n, w = self.selected()
            if w is None:
                return None
            return w.rect().center

        ur(self.key_connect)
        r(self.key_connect, keydown_noarg(_end_connect))
        self._connector_start_pos = _start_pos
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
                def _start_pos():
                    return widget.rect().center
                self._connect_source_node = node
                self._connector_start_pos = _start_pos
                self._connector_end_pos = pygame.mouse.get_pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if self._connect_source_node is not None:
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
        pickle.dump(self.nodes,f,2)

    def _load(self):
        '''Load'''
        import pickle
        f=open('save.pkl', 'rb')
        nodes = pickle.load(f)
        for node in tuple(self.nodes):
            self.remove_node(node)
        self._set_next_keymap()
        for node in nodes:
            self.add_node(node)
            

    def _export_dot(self):
        '''Export the graph to a .dot file'''
        d = Graph.generate_dot(self.generate_groups())
        print d
        open('save.dot', 'wb').write(d)

    def _export_snapshot(self):
        '''Export the graph to a snapshot image'''
        self._save_next_display_update = 'snapshot.bmp'
