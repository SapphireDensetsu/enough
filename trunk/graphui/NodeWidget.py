import pygame
import draw
from guilib import MovingValue
from Lib.Point import Point
from Widget import Widget
from TextEdit import TextEdit, TextStyle
from Keymap import Key
import Keymap

from Lib.observer import Observable

def _make_style(color=(220, 220, 220), font_size=16, font_name='fonts/FreeSansBold.ttf',
                bgcolor=None, is_italic=False, is_underline=False, is_bold=False):
    return TextStyle(color, font_size, font_name, bgcolor,
                     is_italic, is_underline, is_bold)

style = _make_style()

class NodeWidget(Widget):
    bg_color=(10,10,150)
    fg_color=(30,30,150)
    activated_fg_color=(100,100,250)
    
    def __init__(self, node, *args, **kw):
        self.node = node
        
        self.text_widget = TextEdit(style, self._get_text, self._set_text, [Keymap.all_printable])
        
        self.node.obs.add_observer(self, '_node_')
        Widget.__init__(self, *args, **kw)
        
        self._size = MovingValue(Point((20,20)), Point((20,20)))
        self._pos = MovingValue(Point((20,20)), Point((20,20)))
        from Shapes.Ellipse import Ellipse
        self.shape = Ellipse(pygame.Rect(0,0,1,1))

        self.obs_loc = Observable()
        
        r = self.focus_keymap.register_key_noarg
        r(Key(pygame.KMOD_CTRL, pygame.K_RIGHT), self._move_right)
        r(Key(pygame.KMOD_CTRL, pygame.K_LEFT), self._move_left)
        r(Key(pygame.KMOD_CTRL, pygame.K_UP), self._move_up)
        r(Key(pygame.KMOD_CTRL, pygame.K_DOWN), self._move_down)

        r(Key(0, pygame.K_RETURN), self._edit_value)
        self.keymap.register_key_noarg(Key(0, pygame.K_ESCAPE), self._stop_edit_value)

    def in_bounds(self, p):
        return self.rect().collidepoint(tuple(p))
        
    def _get_text(self):
        if self.node.value is None:
            return ''
        return str(self.node.value)
    def _set_text(self, text):
        self.node.value = text
        
    def get_size(self):
        return self._size.current
    def set_size(self, p):
        p = Point(p)
        self._size.final = p
        self.obs_loc.notify.size_set(p)
    size = property(get_size, set_size)
    
    def get_pos(self):
        return self._pos.current
    def set_pos(self, p):
        p = Point(p)
        self._pos.final = p
        self.obs_loc.notify.pos_set(p)
    pos = property(get_pos, set_pos)

    def rect(self):
        s = self.size
        return pygame.Rect(self.pos.x,self.pos.y,s.x,s.y)
    def final_rect(self):
        s = self._size.final
        p = self._pos.final
        return pygame.Rect(p.x,p.y,s.x,s.y)
        
    def _node_connect(self, e):
        pass
    def _node_disconnect(self, e):
        pass
    
        
    def update(self):
        self.text_widget.update()
        self._size.update()
        self._pos.update()
        self.shape.rect = self.rect()
        
    def _draw(self, surface, pos_offset):
        self.shape.paint(pos_offset, surface, self.fg_color, self.bg_color)
        self.text_widget.draw(surface, tuple(Point(pos_offset + Point(self.rect().center) - Point(self.text_widget.size)/2)))
        

    def _move_right(self):
        '''move right'''
        self.pos = self.pos + Point((5,0))
    def _move_left(self):
        '''move left'''
        self.pos = self.pos + Point((-5,0))
    def _move_up(self):
        '''move up'''
        self.pos = self.pos + Point((0,-5))
    def _move_down(self):
        '''move down'''
        self.pos = self.pos + Point((0,5))
        
    def _edit_value(self):
        '''Edit value'''
        self.keymap.set_next_keymap(self.text_widget.focus_keymap)
        self.text_widget._start_editing()

    def _stop_edit_value(self):
        '''Stop editing value'''
        self.text_widget._stop_editing()
        self.keymap.set_next_keymap(self.focus_keymap)
