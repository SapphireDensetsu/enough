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
    def __init__(self, *args, **kw):
        super(GraphWidget, self).__init__(*args, **kw)
        self.out_connection_lines = []
        
    def set_node(self, node):
        self.node = node
        node.value.widget = self

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
        
        #for w in self.iter_visible_connected('in'):
        #    pygame.draw.aalines(surface, (200,20,50), False, (self.connect_pos().as_tuple(), w.connect_pos().as_tuple()), True)
        for line in self.out_connection_lines:
            pygame.draw.aalines(surface, (200,20,50), False, line, True)
            #for p in line:
            #    pygame.draw.circle(surface, (200,50,50), p, 2, 0)

    def paint(self, surface):
        if self.params.visible:
            self.paint_connections(surface)
        super(GraphWidget, self).paint(surface)
        
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
            node.value.widget.pos.final.x = n_layout['x'] * x_scale/1.2
            node.value.widget.pos.final.y = n_layout['y'] * y_scale/1.2

        for node, n_layout in n.iteritems():
            lines = []
            if node not in e:
                continue
            for edge in e[node]:
                this = node.value.widget
                other = edge['tail_node'].value.widget
                
                line = [(int(p[0]*x_scale/1.2), int(p[1]*y_scale/1.2)) for p in edge['points']]
                if (Point.from_tuple(line[0]) - this.pos.final).norm() > (Point.from_tuple(line[-1]) - this.pos.final).norm():
                    line.reverse()
                from Lib.Bezier import Bezier
                line = Bezier(line, 16)
                
                line.insert(0, (this.pos.final.x, this.pos.final.y))
                line.append((other.pos.final.x, other.pos.final.y))
                
                lines.append(line)
            node.value.widget.out_connection_lines = lines
            
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
            if (random.random() > 0.8):
                n1.connect_in(random.choice(nodes))
        nodes.append(n1)

    a.add_nodes(nodes)
    
    a.run()

if __name__=='__main__':
    test()
