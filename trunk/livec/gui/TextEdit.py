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
    margin = [0, 0]
    start_editing_key = Keymap.Key(0, pygame.K_RETURN)
    stop_editing_key = Keymap.Key(0, pygame.K_ESCAPE)
    def __init__(self, style, get_text, set_text=None, groups=None, convertor=None):
        Widget.__init__(self)
        self.get_text = get_text
        self.set_text = set_text
        self.convertor = convertor
        self.key_groups = groups
        if set_text:
            assert self.key_groups, "Must set groups when used in edit mode"
            self.selectable = True
            self._register_keys()
        self.set_style(style)

        # TODO: Debuggability hack
        if get_text() is None:
            import pdb;pdb.set_trace()

    def _register_keys(self):
        self.focus_keymap.register_keydown_noarg(self.start_editing_key,
                                                 self._start_editing)
        self.focus_keymap.register_keydown_noarg(self.stop_editing_key,
                                                 self._stop_editing)

        self.editing_keymap = Keymap.Keymap()
        self.editing_keymap.obs_activation.add_observer(self, "_editing_")
        self.editing_keymap.register_keydown_noarg(Keymap.Key(0, pygame.K_BACKSPACE),
                                                   self._backspace)
        for group in self.key_groups:
            self.editing_keymap.register_group(group,
                                               self._insert_char)

    def _editing_activated(self):
        self.push_frame(bg_color=(40, 80, 40))

    def _editing_deactivated(self):
        self.pop_frame()

    def lost_focus(self):
        Widget.lost_focus(self)
        self._stop_editing()

    def _start_editing(self):
        """Start editing mode"""
        self.focus_keymap.set_next_keymap(self.editing_keymap)

    def _stop_editing(self):
        """Stop editing mode"""
        self.focus_keymap.set_next_keymap(None)

    def _backspace(self):
        """Delete last character"""
        self.set_text(self.get_text()[:-1])

    def _insert_char(self, event):
        """Insert character"""
        self._insert(event.unicode)

    def _insert(self, x):
        self.set_text(self.get_text() + x)

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
        def func(line, curpos):
            return self._font.size(line)
        self.size = self._do(func)
    
    def _draw(self, surface, pos):
        def func(line, curpos):
            text_surface = self._font.render(line, True, self.color, *self.bgcolor)
            gui.draw.draw_font(surface, text_surface,
                               (pos[0]+curpos[0],
                                pos[1]+curpos[1]))
            return self._font.size(line)
        self._do(func)

    def _convert(self, text):
        if self.convertor is None:
            return text
        return ''.join([self.convertor.get(i, i) for i in text])

    def _do(self, func):
        text = self._convert(self.get_text())
        pos = [self.margin[0], self.margin[1]]
        max_width = 0
        for line in text.split('\n'):
            twidth, theight = func(line, pos)
            max_width = max(max_width, twidth + self.margin[0]*2)
            pos[1] += theight + self.margin[1]*2
        return (max_width, pos[1])

def make_label(style, text, selectable=False):
    te = TextEdit(style, lambda : text)
    te.selectable = selectable
    return te
