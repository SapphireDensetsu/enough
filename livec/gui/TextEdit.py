import pygame
from Widget import Widget
import Keymap
import gui.draw

class TextStyle(object):
    def __init__(self, color, font_size, font_name, bgcolor,
                 is_italic, is_underline, is_bold):
        self.color = color
        self.font_size = font_size
        self.font_name = font_name
        self.bgcolor = bgcolor
        self.is_italic = is_italic
        self.is_underline = is_underline
        self.is_bold = is_bold
    
    @classmethod
    def from_style(cls, style):
        return cls(style.color, style.font_size, style.font_name, style.bgcolor,
                   style.is_italic, style.is_underline, style.is_bold)

class TextEdit(Widget):
    selectable = False
    margin = [0, 0]
    start_editing_key = Keymap.Key(0, pygame.K_RETURN)
    stop_editing_key = Keymap.Key(0, pygame.K_ESCAPE)
    cursor_color = (255, 10, 10)
    
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
        self._cursor = None
        self.is_editing = False

    def _register_keys(self):
        self.focus_keymap.register_key_noarg(self.start_editing_key, self._start_editing)

        self.editing_keymap = Keymap.Keymap()
        self.editing_keymap.obs_activation.add_observer(self, "_editing_")
        self.editing_keymap.register_key_noarg(Keymap.Key(0, pygame.K_LEFT), self._left)
        self.editing_keymap.register_key_noarg(Keymap.Key(0, pygame.K_RIGHT), self._right)
        self.editing_keymap.register_key_noarg(Keymap.Key(0, pygame.K_HOME), self._home)
        self.editing_keymap.register_key_noarg(Keymap.Key(0, pygame.K_END), self._end)
        self.editing_keymap.register_key_noarg(Keymap.Key(pygame.KMOD_CTRL, pygame.K_a), self._home)
        self.editing_keymap.register_key_noarg(Keymap.Key(pygame.KMOD_CTRL, pygame.K_e), self._end)
        self.editing_keymap.register_key_noarg(Keymap.Key(0, pygame.K_BACKSPACE), self._backspace)
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
        self.focus_keymap.unregister_key(self.start_editing_key)
        self.focus_keymap.register_key_noarg(self.stop_editing_key, self._stop_editing)
        self.focus_keymap.set_next_keymap(self.editing_keymap)
        self.is_editing = True

    def _stop_editing(self):
        """Stop editing mode"""
        if not self.is_editing:
            return
        self.focus_keymap.unregister_key(self.stop_editing_key)
        self.focus_keymap.register_key_noarg(self.start_editing_key, self._start_editing)
        self.is_editing = False
        self.focus_keymap.set_next_keymap(None)
        self._cursor = None

    def _home(self):
        """Go to beginning of line"""
        self._cursor = 0

    def _end(self):
        """Go to end of line"""
        self._cursor = len(self.get_text())

    def _left(self):
        """Go left once"""
        self._fix_cursor()
        if self._cursor > 0:
            self._cursor -= 1

    def _right(self):
        """Go right once"""
        self._fix_cursor()
        if self._cursor < len(self.get_text()):
            self._cursor += 1

    def _backspace(self):
        """Delete last character"""
        self._fix_cursor()
        o = self.get_text()
        self.set_text(o[:self._cursor-1] + o[self._cursor:])
        self._cursor -= 1

    def _insert_char(self, event):
        """Insert character"""
        self._insert(event.unicode)

    def _insert(self, x):
        self._fix_cursor()
        o = self.get_text()
        self.set_text(o[:self._cursor] + x + o[self._cursor:])
        self._cursor += 1

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
        self._font.set_italic(style.is_italic)
        self._font.set_underline(style.is_underline)
        self._font.set_bold(style.is_bold)

    def update(self):
        def func(index, atom, curpos):
            return self._font.size(atom)
        self.size = self._do(func)

    def _fix_cursor(self):
        if self._cursor is None:
            self._cursor = len(self.get_text())
    
    def _draw(self, surface, pos):
        self._fix_cursor()
        def func(index, atom, curpos):
            text_surface = self._font.render(atom, True, self.color, *self.bgcolor)
            size = self._font.size(atom)
            abspos = tuple(a+b for a, b in zip(pos, curpos))
            if self.is_editing and index == self._cursor:
                gui.draw.line(surface, self.cursor_color, abspos,
                              (abspos[0], abspos[1]+size[1]), 2)
            gui.draw.draw_font(surface, text_surface, abspos)
            return size
        self._do(func)

    def _convert(self, text):
        if self.convertor is None:
            return list(text)
        return [self.convertor.get(i, i) for i in text]

    def _do(self, func):
        text = self._convert(self.get_text())
        pos = [self.margin[0], self.margin[1]]
        max_width = pos[0]
        for index, atom in enumerate(text + ['']):
            if '\n' in atom:
                assert atom == '\n', "Newlines inside atoms not supported"
                pos[0] = self.margin[0]
                pos[1] += theight + self.margin[1]*2
                continue
            twidth, theight = func(index, atom, pos)
            pos[0] += twidth + self.margin[0]
            max_width = max(max_width, pos[0])
        return (max_width, pos[1] + theight + self.margin[1])

def make_label(style, text, selectable=False):
    te = TextEdit(style, lambda : text)
    te.selectable = selectable
    return te
