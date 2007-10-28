# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from ccode import c_escape_char
from LiteralWidget import LiteralWidget
from gui import Keymap
import style
import struct
import pygame

class LiteralIntWidget(LiteralWidget):
    escape_table = None
    ldelimiter = ""
    rdelimiter = ""
    ldelimiter_style = rdelimiter_style = style.literal_int
    literal_style = style.literal_int
    example_style = style.example_int
    _mode = 'dec'
    
    hex_mode_key = Keymap.Key(pygame.KMOD_CTRL, pygame.K_x)
    dec_mode_key = Keymap.Key(pygame.KMOD_CTRL, pygame.K_d)
    oct_mode_key = Keymap.Key(pygame.KMOD_CTRL, pygame.K_o)

    def __init__(self, literal):
        LiteralWidget.__init__(self, literal)
        self.keymap.register_key(self.hex_mode_key, Keymap.keydown_noarg(self._set_hex_mode))
        self.keymap.register_key(self.dec_mode_key, Keymap.keydown_noarg(self._set_dec_mode))
        self.keymap.register_key(self.oct_mode_key, Keymap.keydown_noarg(self._set_oct_mode))

    def _set_mode(self, new_mode, ldelimiter):
        self._mode = new_mode
        self.ldelimiter = ldelimiter
        self.text_edit.set_cursor(len(self._get_string()))
        
    def _set_hex_mode(self):
        """Hex mode"""
        self._set_mode('hex', '0x')

    def _set_dec_mode(self):
        """Decimal mode"""
        self._set_mode('dec', '')
        
    def _set_oct_mode(self):
        """Octal mode"""
        self._set_mode('oct', '0')
    
    def _get_example_str(self):
        int_val = self.literal.value
        return '%d\n0x%X\n0%o' % (int_val, int_val, int_val)

    def _value_of_string(self, text):
        return getattr(self, '_%s__value_of_string' % (self._mode,))(text)
    def _string_of_value(self, value):
        return getattr(self, '_%s__string_of_value' % (self._mode,))(value)
    def _allowed_text(self, text):
        is_allowed = getattr(self, '_%s__allowed_text' % (self._mode,))(text)
        if not is_allowed:
            return False
        value = self._value_of_string(text)
        transformed_text = self._string_of_value(value)
        return transformed_text == text

    def _dec__value_of_string(self, text):
        if not text:
            return 0
        return int(text)
    def _dec__string_of_value(self, value):
        return str(value)
    def _dec__allowed_text(self, value):
        return value.isdigit()

    def _oct__value_of_string(self, text):
        if not text:
            return 0
        return int(text, 8)
    def _oct__string_of_value(self, value):
        return oct(long(value))[1:-1]
    def _oct__allowed_text(self, value):
        return all(c in '01234567' for c in value)

    def _hex__value_of_string(self, text):
        if not text:
            return 0
        return int(text, 16)
    def _hex__string_of_value(self, value):
        return hex(long(value))[2:-1]
    def _hex__allowed_text(self, value):
        return all((c.isdigit() or c in 'abcdef')
                   for c in value.lower())
