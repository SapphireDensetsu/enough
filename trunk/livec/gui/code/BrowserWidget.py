import itertools
import weakref
from gui.Stack import Stack
from gui.Keymap import Key
import gui.draw
import pygame

class BrowserWidget(Stack):
    def __init__(self):
        Stack.__init__(self)
        self.index_gen = itertools.count()
        self._names = weakref.WeakKeyDictionary()

        def register_ctrl_key(x, func):
            self.keymap.register_keydown_noarg(Key(pygame.KMOD_CTRL, x), func)
        register_ctrl_key(pygame.K_LEFT, self._offset_right)
        register_ctrl_key(pygame.K_RIGHT, self._offset_left)
        register_ctrl_key(pygame.K_UP, self._offset_down)
        register_ctrl_key(pygame.K_DOWN, self._offset_up)

    offset_speed = 25
    def _offset_left(self):
        """Moves screen left"""
        gui.draw.offset.add_offset((self.offset_speed,0))
    def _offset_right(self):
        """Moves screen right"""
        gui.draw.offset.add_offset((-self.offset_speed,0))
    def _offset_up(self):
        """Moves screen up"""
        gui.draw.offset.add_offset((0,self.offset_speed))
    def _offset_down(self):
        """Moves screen down"""
        gui.draw.offset.add_offset((0,-self.offset_speed))

    def get_name(self, x):
        if x not in self._names:
            self._names[x] = 'name_%d' % (self.index_gen.next(),)
        return self._names[x]
