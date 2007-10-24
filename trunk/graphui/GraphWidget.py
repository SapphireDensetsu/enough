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
        
        r = self.focus_keymap.register_key_noarg
        r(Key(0, pygame.K_RIGHT), self._next_node)
        r(Key(0, pygame.K_LEFT), self._prev_node)

    def get_size(self):
        return self._size.current
    def set_size(self, p):
        self._size.final = p 
    size = property(get_size, set_size)
    
    def _node_connect(self, e):
        for node in e.source, e.target:
            if node not in self.nodes:
                self.new_node(node)
        if e not in self.edges:
            self.new_edge(e)
    def _node_disconnect(self, e):
        self.remove_edge(e)
        for node in e.source, e.target:
            self.remove_node(node)

    def new_edge(self, edge):
        self.edges.add(edge)
        #w = EdgeWidget(edge)
        #self.widgets[edge] = w
    def remove_node(self, node):
        #del self.widgets[node]
        self.nodes.remove(node)

    def new_node(self, node):
        self.nodes.add(node)
        w = NodeWidget(node)
        self.widgets[node] = w
    def remove_node(self, node):
        del self.widgets[node]
        self.nodes.remove(node)
        
    def update(self):
        for w in self.widgets.values():
            w.update()
        self._size.update()
        
        
    def _draw(self, surface, pos):
        for w in self.widgets.values():
            # for our children, pos is the parent's pos offset
            # because of how NodeWidget works.
            w._draw(surface, pos)


    # -----------------------------------
    def selected_child(self):
        node, widget = self.sorted_widgets[self.selected_widget_index]
        return widget
    
    def _set_selected_widget(self):
        self.focus_keymap.set_next_keymap(self.selected_child().keymap)
        
    def _add_index(self, amount):
        prev = self.selected_widget_index
        if not self.selected_widget_index and self.widgets:
            self.selected_widget_index = 0
        else:
            l = len(self.sorted_widgets)
            self.selected_widget_index += amount
            self.selected_widget_index %= l

        if prev != self.selected_widget_index:
            self._set_selected_widget()
        
    def _next_node(self):
        '''Next node'''
        self._add_index(1)
    def _prev_node(self):
        '''Previous node'''
        self._add_index(-1)
                
