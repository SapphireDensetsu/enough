# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from ccode import c_escape_char
from LiteralWidget import LiteralWidget
import style
import struct

class LiteralCharWidget(LiteralWidget):
    escape_table = c_escape_char
    ldelimiter = rdelimiter = "'"
    ldelimiter_style = rdelimiter_style = style.literal_char_delimiter
    literal_style = style.literal_char
    example_style = style.example_char_int
    
    def _get_example_str(self):
        s = self.literal.value
        full = s.ljust(4, '\x00')
        assert len(full) == 4
        int_val, = struct.unpack('<L', full)
        return '%d\n0x%X' % (int_val, int_val)

    def _allowed_text(self, value):
        return len(value) <= 4
