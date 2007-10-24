import pygame
import draw
from guilib import MovingValue
from Lib.Point import Point
from Widget import Widget


class NodeWidget(Widget):
    bg_color=(10,10,150)
    fg_color=(30,30,150)
    activated_fg_color=(100,100,250)
    
    def __init__(self, node, *args, **kw):
        self.node = node
        self.node.obs.add_observer(self, '_node_')
        Widget.__init__(self, *args, **kw)
        
        self._size = MovingValue(Point((20,20)), Point((20,20)))
        self._pos = MovingValue(Point((20,20)), Point((20,20)))
        from Shapes.Ellipse import Ellipse
        self.shape = Ellipse(pygame.Rect(0,0,1,1))


    def get_size(self):
        return self._size.current
    def set_size(self, p):
        self._size.final = Point(p)
    size = property(get_size, set_size)
    
    def get_pos(self):
        return self._pos.current
    def set_pos(self, p):
        self._pos.final = Point(p)
    pos = property(get_pos, set_pos)
    
    def _node_connect(self, e):
        pass
    def _node_disconnect(self, e):
        pass
    
        
    def update(self):
        self._size.update()
        self._pos.update()
        s = self.size
        self.shape.rect = pygame.Rect(self.pos.x,self.pos.y,s.x,s.y)
        
    def _draw(self, surface, pos_offset):
        self.shape.paint(pos_offset, surface, self.fg_color, self.bg_color)
        
