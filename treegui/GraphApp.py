import pygame
from App import App
from Widget import Widget
from Lib import Graph

from Lib.Point import Point

class NodeValue(object):
    widget = None
    
class GraphWidget(Widget):
    def set_node(self, node):
        self.params.user = node
        node.value.widget = self

    def paint(self, surface):
        if self.params.visible:
            self.paint_connections(surface)
        super(GraphWidget, self).paint(surface)

    def connect_pos(self, upper=False):
        y = self.size.current.y * 0.5
        return self.pos.current + Point(self.size.current.x * 0.5, y)
    
    def paint_connections(self, surface):
        if self.params.user is None:
            return

        for out_node in self.params.user.connections['out']:
            w = out_node.value.widget
            if not w.params.visible:
                continue
            pygame.draw.aalines(surface, (200,20,50), False, (self.connect_pos().as_tuple(), w.connect_pos().as_tuple()), True)
        
        
class GraphApp(App):
    def add_nodes(self, nodes):
        for node in nodes:
            w = GraphWidget()
            w.set_node(node)
            self.add_widget(w)


#---------------------------------------------

class TestNodeValue(NodeValue):
    def __init__(self, name):
        self.name = name

    def set_widget(self, widget):
        self._widget = widget
        self.update_widget_text()
    def get_widget(self):
        return self._widget
    widget = property(fget=get_widget,fset=set_widget)
    
    def update_widget_text(self):
        print 'here'
        self._widget.text = self.name

def test():
    a = GraphApp()

    n1 = Graph.Node(TestNodeValue('moshe'))
    n2 = Graph.Node(TestNodeValue('yosi'))
    n1.connect_out(n2)

    a.add_nodes((n1, n2))
    
    a.run()

if __name__=='__main__':
    test()
