# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from ccode import c_escape_str
from LiteralWidget import LiteralWidget
import style

class LiteralStrWidget(LiteralWidget):
    escape_table = c_escape_str
    ldelimiter = rdelimiter = '"'
    ldelimiter_style = rdelimiter_style = style.literal_string_delimiter
    literal_style = style.literal_string
    example_frame_color = (255, 255, 255)
    example_style = style.example_string

    def _get_example_str(self):
        return self._get_string()
