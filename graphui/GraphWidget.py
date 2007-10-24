import pygame
import draw
from guilib import MovingValue
from Lib.Point import Point
from Widget import Widget
from NodeWidget import NodeWidget

from Lib import observer

from Keymap import Keymap, Key

from Lib.observable.SortedItems import SortedItems
from Lib.observable.Dict import Dict

from Lib import Graph

class GraphWidget(Widget):
    bg_color=(0,0,0)
    activated_bg_color=(10,10,20)
    def __init__(self, size, *args, **kw):
        Widget.__init__(self, *args, **kw)
        self._size = MovingValue(Point((0,0)), Point(size))
        self.nodes = set()
        self.edges = set()
        self.widgets = Dict()
        self.widgets.obs = observer.Observable()
        self.sorted_widgets = SortedItems(self.widgets)

        self.selected_widget_index = None

        self.parenting_keymap = Keymap()
        self._set_next_keymap()
        
        r = self.parenting_keymap.register_key_noarg
        r(Key(0, pygame.K_RIGHT), self._next_node)
        r(Key(0, pygame.K_LEFT), self._prev_node)
        r(Key(pygame.KMOD_CTRL, pygame.K_a), self._create_new_node)

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
        for node in e.source, e.target:
            self.remove_node(node)

    def add_edge(self, edge):
        self.edges.add(edge)
        #w = EdgeWidget(edge)
        #self.widgets[edge] = w
    def remove_node(self, node):
        #del self.widgets[node]
        self.nodes.remove(node)

    def add_node(self, node):
        self.nodes.add(node)
        w = NodeWidget(node)
        self.widgets[node] = w
        return w
    def remove_node(self, node):
        w = self.widgets[node]
        del self.widgets[node]
        self.nodes.remove(node)
        return w
        
    def update(self):
        for w in self.widgets.values():
            w.update()
        self._size.update()
        
        
    def _draw(self, surface, pos):
        for w in self.widgets.values():
            # for our children, pos is the parent's pos offset
            # because of how NodeWidget works.
            w._draw(surface, pos)

    def selected_child(self):
        node, widget = self.sorted_widgets[self.selected_widget_index]
        return widget
    
    def _set_next_keymap(self):
        self.keymap.set_next_keymap(self.parenting_keymap)
        if self.selected_widget_index is not None:
            self.parenting_keymap.set_next_keymap(self.selected_child().keymap)
        else:
            self.parenting_keymap.set_next_keymap(self.focus_keymap)
    
    def _set_selected_widget(self, index = None):
        if index is None:
            index = self.selected_widget_index
        else:
            self.selected_widget_index = index
        self._set_next_keymap()

    def _find_widget_index(self, w):
        for i, (node, widget) in enumerate(self.sorted_widgets):
            if w == widget:
                return i
            
    def _add_index(self, amount):
        if self.selected_widget_index is None:
            if not self.widgets:
                return
            index = 0
        else:
            index = self.selected_widget_index
            l = len(self.sorted_widgets)
            index += amount
            index %= l
        self._set_index(index)

    def _set_index(self, index):
        if self.selected_widget_index != index:
            self.selected_widget_index = index
            self._set_selected_widget()

    def _next_node(self):
        '''Next node'''
        self._add_index(1)
    def _prev_node(self):
        '''Previous node'''
        self._add_index(-1)

    def _create_new_node(self):
        '''Create new node'''
        n = Graph.Node()
        w = self.add_node(n)
        self._set_index(self._find_widget_index(w))
        
        
