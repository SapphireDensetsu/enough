# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from ccode import c_escape_char
from LiteralWidget import LiteralWidget
import style
import struct

class LiteralIntWidget(LiteralWidget):
    escape_table = None
    delimiter = ""
    literal_style = style.literal_int
    delimiter_style = style.literal_int
    example_style = style.example_int
    
    def _get_example_str(self):
        int_val = self.literal.value
        return '%d\n0x%X' % (int_val, int_val)

    def _value_of_string(self, value):
        return int(value)
    def _string_of_value(self, value):
        return str(value)

    def allowed_text(self, value):
        return value.isdigit()
