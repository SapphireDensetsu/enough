import pygame
import draw
from guilib import MovingValue
from Lib.Point import Point
from Widget import Widget
from NodeWidget import NodeWidget

class GraphWidget(Widget):
    bg_color=(0,0,0)
    activated_bg_color=(10,10,20)
    def __init__(self, size, *args, **kw):
        Widget.__init__(self, *args, **kw)
        self._size = MovingValue(Point((0,0)), Point(size))
        self.nodes = set()
        self.edges = set()
        self.widgets = {}

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
