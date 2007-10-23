import pygame
from Widget import Widget
import gui.draw

class TextStyle(object):
    def __init__(self, color, font_size, font_name, bgcolor=None):
        self.color = color
        self.font_size = font_size
        self.font_name = font_name
        self.bgcolor = bgcolor
    
    @classmethod
    def from_style(cls, style):
        return cls(style.color, style.font_size, style.font_name, style.bgcolor)

class TextEdit(Widget):
    selectable = False
    def __init__(self, style, get_text, set_text=None):
        Widget.__init__(self)
        self.get_text = get_text
        self.set_text = set_text
        if set_text:
            self.selectable = True
        self.color = style.color
        if style.bgcolor is None:
            self.bgcolor = ()
        else:
            self.bgcolor = (style.bgcolor,)
        try:
            self._font = gui.draw.get_font(style.font_name, style.font_size)
        except IOError:
            self._font = gui.draw.get_font(pygame.font.get_default_font(), style.font_size)

    def update(self):
        def func(line, cur_height):
            return self._font.size(line)
        self.size = self._do(func)
    
    def _draw(self, surface, pos):
        def func(line, cur_height):
            text_surface = self._font.render(line, True, self.color, *self.bgcolor)
            gui.draw.draw_font(surface, text_surface, (pos[0], pos[1]+cur_height))
            return self._font.size(line)
        self._do(func)

    def _do(self, func):
        text = self.get_text()
        size = [0, 0]
        for line in text.split('\n'):
            twidth, theight = func(line, size[1])
            size[0] = max(size[0], twidth)
            size[1] += theight
        return size

def make_label(style, text, selectable=False):
    te = TextEdit(style, lambda : text)
    te.selectable = selectable
    return te
