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
    _default_mode = 'dec'
    keymap_group = Keymap.extended_digits
    
    hex_mode_key = Keymap.Key(pygame.KMOD_CTRL, pygame.K_x)
    dec_mode_key = Keymap.Key(pygame.KMOD_CTRL, pygame.K_d)
    oct_mode_key = Keymap.Key(pygame.KMOD_CTRL, pygame.K_o)
    negate_key = Keymap.Key(0, pygame.K_MINUS)

    def __init__(self, literal):
        LiteralWidget.__init__(self, literal)
        self.keymap.register_key(self.hex_mode_key, Keymap.keydown_noarg(self._set_hex_mode))
        self.keymap.register_key(self.dec_mode_key, Keymap.keydown_noarg(self._set_dec_mode))
        self.keymap.register_key(self.oct_mode_key, Keymap.keydown_noarg(self._set_oct_mode))

        self.text_edit.editing_keymap.register_key(
            self.negate_key,
            Keymap.keydown_noarg(self._negate)
        )
        self._set_mode(self.literal.meta.get('mode', self._default_mode))

    def _negate(self):
        """Negate the number"""
        self.literal.value = -self.literal.value
        self._fix_ldelimiter()

    def _set_mode(self, new_mode):
        self.literal.meta['mode'] = new_mode
        self._mode = new_mode
        self.ldelimiter = getattr(self, '_%s__ldelimiter' % (new_mode,))
        self._fix_ldelimiter()
        self.text_edit.set_cursor(len(self._get_string()))

    def _fix_ldelimiter(self):
        ldelimiter = self.ldelimiter.lstrip('-')
        if self.literal.value < 0:
            ldelimiter = '-' + ldelimiter
        self.ldelimiter = ldelimiter
        
    def _set_hex_mode(self):
        """Hex mode"""
        self._set_mode('hex')

    def _set_dec_mode(self):
        """Decimal mode"""
        self._set_mode('dec')
        
    def _set_oct_mode(self):
        """Octal mode"""
        self._set_mode('oct')
    
    def _get_example_str(self):
        if self.literal.value < 0:
            minus = '-'
        else:
            minus = ''
        int_val = abs(self.literal.value)
        return '%s%d\n%s0x%X\n%s0%o' % (minus, int_val,
                                        minus, int_val,
                                        minus, int_val)

    def _value_of_string(self, text):
        if not text:
            return 0
        value = getattr(self, '_%s__value_of_string' % (self._mode,))(text)
        if self.literal.value < 0:
            value = -value
        return value
    def _string_of_value(self, value):
        return getattr(self, '_%s__string_of_value' % (self._mode,))(value)
    def _allowed_text(self, text):
        return getattr(self, '_%s__allowed_text' % (self._mode,))(text)

    def _dec__value_of_string(self, text):
        return int(text)
    def _dec__string_of_value(self, value):
        return str(abs(value))
    def _dec__allowed_text(self, value):
        return not value or value.isdigit()
    _dec__ldelimiter = ''

    def _oct__value_of_string(self, text):
        return int(text, 8)
    def _oct__string_of_value(self, value):
        return oct(long(abs(value)))[1:-1]
    def _oct__allowed_text(self, value):
        return all(c in '01234567' for c in value)
    _oct__ldelimiter = '0'

    def _hex__value_of_string(self, text):
        return int(text, 16)
    def _hex__string_of_value(self, value):
        return hex(long(abs(value)))[2:-1]
    def _hex__allowed_text(self, value):
        return all((c.isdigit() or c in 'abcdef')
                   for c in value.lower())
    _hex__ldelimiter = '0x'
import nodes
from widget_for import NormalWidgetMaker
NormalWidgetMaker.register(nodes.LiteralInt, LiteralIntWidget)
