import pygame
from Widget import Widget
import Keymap
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
    margin=[0,0]
    def __init__(self, style, get_text, set_text=None):
        Widget.__init__(self)
        self.get_text = get_text
        self.set_text = set_text
        if set_text:
            self.selectable = True
            self._register_keys()
        self.set_style(style)

        # TODO: Debuggability hack
        if get_text() is None:
            import pdb;pdb.set_trace()

    def _register_keys(self):
        self.focus_keymap.register_keydown_noarg(Keymap.Key(0, pygame.K_BACKSPACE),
                                                 self._backspace)
        self.focus_keymap.register_group(Keymap.alphanumeric,
                                         self._insert_char)

    def _backspace(self):
        """Backspace"""
        self.set_text(self.get_text()[:-1])

    def _insert_char(self, event):
        """Insert character"""
        self.set_text(self.get_text() + event.unicode)

    def set_style(self, style):
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
            size = list(self._font.size(line))
            size[0] += self.margin[0]*2
            size[1] += self.margin[1]*2
            return size
        self.size = self._do(func)
    
    def _draw(self, surface, pos):
        def func(line, cur_height):
            text_surface = self._font.render(line, True, self.color, *self.bgcolor)
            gui.draw.draw_font(surface, text_surface, (pos[0]+self.margin[0], pos[1]+cur_height+self.margin[1]))
            size = list(self._font.size(line))
            size[0] += self.margin[0]*2
            size[1] += self.margin[1]*2
            return size
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
