import pygame
import random

from App import App
from Widget import Widget
from Lib import Graph

from Lib.Point import Point

from guilib import get_default

class NodeValue(object):
    def __init__(self, name, start_pos=None):
        self.name = name
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

class GraphWidget(Widget):
    def set_node(self, node):
        self.node = node
        node.value.widget = self

    def connect_pos(self, upper=False):
        y = self.size.current.y * 0.5
        return self.pos.current + Point(self.size.current.x * 0.5, y)

        
class GraphApp(App):
    def __init__(self, *args, **kw):
        super(GraphApp, self).__init__(*args, **kw)
        from Lib.Dot import Dot
        self.dot = Dot()
        
    def add_nodes(self, nodes):
        for node in nodes:
            w = GraphWidget()
            w.set_node(node)
            self.add_widget(w)
        self.update_layout()            

    def zoom(self, zoom):
        for widget in self.widgets:
            widget.font_size.final = widget.font_size.final * zoom
        self._paint(None)

    def _paint(self, surface):
        #self.update_layout()
        super(GraphApp, self)._paint(surface)
        
    def _key_up(self, e):
        super(GraphApp, self)._key_up(e)
        if (e.mod & pygame.KMOD_CTRL):
            if e.key == pygame.K_w:
                self.zoom(1.3)
            elif e.key == pygame.K_q:
                self.zoom(1/(1.3))

    def update_layout(self):
        nodes = [widget.node for widget in self.widgets]
        g, n, e = Graph.get_drawing_data(self.dot, nodes)
        x_scale = self.width / float(g['width'])
        y_scale = self.height / float(g['height'])
        for node, n_layout in n.iteritems():
            node.value.widget.pos.final.x = n_layout['x'] * x_scale/2
            node.value.widget.pos.final.y = n_layout['y'] * y_scale/2
            #print node.value.widget.pos.final
            #node.value.widget.size.final.x = n_layout['width']
            #node.value.widget.size.final.y = n_layout['height']
            

#---------------------------------------------


def test():
    a = GraphApp()

    import random
    nodes = []
    for i in xrange(15):
        pos = Point(10*random.random() - 5, 10*random.random() - 5)
        pos = pos + Point(a.width, a.height)*0.5
        n1 = Graph.Node(NodeValue(str(i), pos))
        if nodes:
            n1.connect_out(random.choice(nodes))
            n1.connect_in(random.choice(nodes))
        nodes.append(n1)

    a.add_nodes(nodes)
    
    a.run()

if __name__=='__main__':
    test()
