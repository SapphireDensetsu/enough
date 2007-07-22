import pygame
from App import App
from Widget import Widget
from Lib import Graph

from Lib.Point import Point

class NodeValue(object):
    def __init__(self, name):
        self.name = name

    def set_widget(self, widget):
        self._widget = widget
        self.update_widget_text()
    def get_widget(self):
        return self._widget
    widget = property(fget=get_widget,fset=set_widget)
    
    def update_widget_text(self):
        self._widget.text = self.name
    
class GraphWidget(Widget):
    NEAR_REPEL = 10
    FAR_REPEL  = 70
    NEAR_PULL  = 120
    force_compression = 100
    force_power = 1
    
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

    def iter_visible_widgets(self, dir):
        for out_node in self.params.user.connections[dir]:
            w = out_node.value.widget
            if not w.params.visible:
                continue
            yield w
            
    def paint_connections(self, surface):
        if self.params.user is None:
            return

        for w in self.iter_visible_widgets('in'):
            pygame.draw.aalines(surface, (200,20,50), False, (self.connect_pos().as_tuple(), w.connect_pos().as_tuple()), True)
        

    def update_force_move(self, w):
        diff = w.pos.current - self.pos.current
        force_distance_mul = ((self.size.current + w.size.current) * 0.5).norm() / self.force_compression
        
        if diff.norm() < self.NEAR_REPEL*force_distance_mul:
            force = 0.5
        elif diff.norm() < self.FAR_REPEL*force_distance_mul:
            force = 0.2
        elif diff.norm() < self.NEAR_PULL*force_distance_mul:
            force = 0
        else:
            force = -diff.norm() / 100.0 / 10
        w.pos.final += diff*force*self.force_power
        
    def update_moving(self):
        # calculate repulsion/attraction to other nodes
        for w in self.iter_visible_widgets('out'):
            self.update_force_move(w)
        for w in self.iter_visible_widgets('in'):
            self.update_force_move(w)
            
        super(GraphWidget, self).update_moving()
        
class GraphApp(App):
    def add_nodes(self, nodes):
        for node in nodes:
            w = GraphWidget()
            w.set_node(node)
            self.add_widget(w)

    def zoom(self, zoom):
        for widget in self.widgets:
            widget.font_size.final = widget.font_size.final * zoom
        self._paint(None)

    def compress(self, compression):
        for widget in self.widgets:
            widget.force_compression *= compression
        self._paint(None)
        
    def _key_up(self, e):
        super(GraphApp, self)._key_up(e)
        if (e.mod & pygame.KMOD_CTRL):
            if e.key == pygame.K_w:
                self.zoom(1.3)
            elif e.key == pygame.K_q:
                self.zoom(1/(1.3))
            if e.key == pygame.K_a:
                self.compress(1.3)
            elif e.key == pygame.K_s:
                self.compress(1/(1.3))

#---------------------------------------------


def test():
    a = GraphApp()

    n1 = Graph.Node(NodeValue('moshe'))
    n2 = Graph.Node(NodeValue('yosi'))
    n1.connect_out(n2)

    a.add_nodes((n1, n2))
    
    a.run()

if __name__=='__main__':
    test()
