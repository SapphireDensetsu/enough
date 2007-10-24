from gui.TextEdit import TextEdit
from gui.code.widget_for import widget_for
from gui import Keymap
from lib.observable.List import List
import style

import pygame

class LiteralIntWidget(TextEdit):
    selectable = True
    def __init__(self, literal):
        self.literal = literal
        s = style.literal_style_for[self.literal.__class__]
        TextEdit.__init__(self, s, lambda : str(self.literal.value))

        self.focus_keymap.register_key_noarg(Keymap.Key(0, pygame.K_BACKSPACE), self._backspace)
        self.focus_keymap.register_key_noarg(Keymap.Key(0, pygame.K_MINUS), self._minus)
        self.focus_keymap.register_group(Keymap.digits, self._add_digit)

    def _backspace(self):
        """Remove the last digit from the number"""
        self.literal.value /= 10
        
    def _minus(self):
        """Negate the number"""
        self.literal.value *= -1
        
    def _add_digit(self, event):
        """Add a digit to the number"""
        self.literal.value *= 10
        if self.literal.value >= 0:
            self.literal.value += (event.key - pygame.K_0)
        else:
            self.literal.value -= (event.key - pygame.K_0)
