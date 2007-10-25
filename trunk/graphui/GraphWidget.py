from functools import partial

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

class GraphWidget(Widget):
    bg_color=(0,0,0)
    activated_bg_color=(10,10,20)

    create_node_key = Key(pygame.KMOD_CTRL, pygame.K_a)
    delete_node_key = Key(pygame.KMOD_CTRL, pygame.K_d)
    connect_node_right_key = Key(pygame.KMOD_SHIFT, pygame.K_RIGHT)
    
    def __init__(self, size, *args, **kw):
        Widget.__init__(self, *args, **kw)
        self._size = MovingValue(Point((0,0)), Point(size))
        self.nodes = set()
        self.edges = set()
        self.node_widgets = Dict()
        self.edge_widgets = Dict()
        self.sorted_widgets = SortedItems(self.node_widgets)

        self.selected_widget_index = None

        self.parenting_keymap = Keymap()
        self._set_next_keymap()
        
        r = self.parenting_keymap.register_key_noarg
        r(Key(0, pygame.K_TAB), self._next_node)
        r(Key(pygame.KMOD_SHIFT, pygame.K_TAB), self._prev_node)
        r(Key(0, pygame.K_RIGHT), self._select_node_right)
        r(Key(0, pygame.K_LEFT), self._select_node_left)
        r(Key(0, pygame.K_UP), self._select_node_up)
        r(Key(0, pygame.K_DOWN), self._select_node_down)
        r(self.create_node_key, self._create_new_node)

        self.layout = Layout()

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
                       MovingLine([Point((0,0)), Point((1,1))], [Point(source), Point(target)]))
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

    def update_layout(self):
        groups = {'0':[]}
        for node in self.nodes:
            groups['0'].append(node) 
        self.layout.update(groups, self.size, self.node_widgets, self.edge_widgets)
        
    def update(self):
        for w in self.node_widgets.values():
            w.update()
        for w in self.edge_widgets.values():
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

    def selected(self):
        if self.selected_widget_index is None:
            return None, None
        return self.sorted_widgets[self.selected_widget_index]
    
    def _set_next_keymap(self):
        self.keymap.set_next_keymap(self.parenting_keymap)
        if self.selected_widget_index is not None:
            self.parenting_keymap.set_next_keymap(self.selected()[1].keymap)
            r = self.parenting_keymap.register_key_noarg
            r(self.delete_node_key, self._delete_selected_node)
            r(self.connect_node_right_key, self._connect_right)
        else:
            self.parenting_keymap.unregister_key(self.delete_node_key)
            self.parenting_keymap.unregister_key(self.connect_node_right_key)
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
        
        
    def _connect_right(self):
        '''Connects to the node on the right'''
        node, widget = self.sorted_widgets[self.selected_widget_index]
        n1 = self.selected()[0]
        self._next_node()
        n2 = self.selected()[0]

        n1.connect_node(n2)
        
