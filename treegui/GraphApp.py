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
    NEAR_REPEL = 10
    FAR_REPEL  = 20
    NEAR_PULL  = 80
    force_compression = 10
    force_power = 1
    
    def set_node(self, node):
        self.node = node
        node.value.widget = self
    def set_repel_list(self, l):
        self.repelled_widgets = l
    def paint(self, surface):
        if self.params.visible:
            self.paint_connections(surface)
        super(GraphWidget, self).paint(surface)

    def connect_pos(self, upper=False):
        y = self.size.current.y * 0.5
        return self.pos.current + Point(self.size.current.x * 0.5, y)

    def iter_visible_nodes(self, nlist):
        for out_node in nlist:
            w = out_node.value.widget
            if not w.params.visible:
                continue
            yield w
    def iter_visible_connected(self, dir):
        for w in self.iter_visible_nodes(self.node.connections[dir]):
            yield w
            
    def paint_connections(self, surface):
        if self.node is None:
            return

        for w in self.iter_visible_connected('in'):
            pygame.draw.aalines(surface, (200,20,50), False, (self.connect_pos().as_tuple(), w.connect_pos().as_tuple()), True)
        

    def update_force_move(self, w, repel, pull):
        diff = w.pos.current - self.pos.current
        force_distance_mul = ((self.font_size.current + w.font_size.current) * 0.5) / self.force_compression 
        force = 0
        d = diff.norm()
        if repel:
            if d < self.NEAR_REPEL*force_distance_mul:
                force = 0.5
            elif d < self.FAR_REPEL*force_distance_mul:
                force = 0.2
                
        if pull:
            if d < self.NEAR_PULL*force_distance_mul:
                force = 0
            else:
                force = -d / 100.0 / 10
        w.pos.final += diff*force*self.force_power
        
    def update_moving(self):
        # calculate repulsion/attraction to other nodes
        for w in self.iter_visible_connected('out'):
            self.update_force_move(w, False, True)
        for w in self.iter_visible_connected('in'):
            self.update_force_move(w, False, True)
        for w in self.repelled_widgets:
            self.update_force_move(w, True, False)
        super(GraphWidget, self).update_moving()
        
class GraphApp(App):
    forces = True
    def add_nodes(self, nodes):
        for node in nodes:
            w = GraphWidget()
            w.set_node(node)
            self.add_widget(w)
            w.set_repel_list(self.widgets)

    def zoom(self, zoom):
        for widget in self.widgets:
            widget.font_size.final = widget.font_size.final * zoom
        self._paint(None)

    def compress(self, compression):
        for widget in self.widgets:
            widget.force_compression *= compression
        self._paint(None)

    def update_forces(self):
        if self.forces:
            force_power = 1
        else:
            force_power = 0
        for widget in self.widgets:
            widget.force_power = force_power
            
    def _key_up(self, e):
        super(GraphApp, self)._key_up(e)
        if (e.mod & pygame.KMOD_CTRL):
            if e.key == pygame.K_w:
                self.zoom(1.3)
            elif e.key == pygame.K_q:
                self.zoom(1/(1.3))
            elif e.key == pygame.K_a:
                self.compress(1.3)
            elif e.key == pygame.K_s:
                self.compress(1/(1.3))
            elif e.key == pygame.K_x:
                if self.focused_widget:
                    self.focused_widget.force_power = 1
                if (e.mod & pygame.KMOD_SHIFT):
                    self.forces = True
                    self.update_forces()
            elif e.key == pygame.K_c:
                if self.focused_widget:
                    self.focused_widget.force_power = 0
                if (e.mod & pygame.KMOD_SHIFT):
                    self.forces = False
                    self.update_forces()
            

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
