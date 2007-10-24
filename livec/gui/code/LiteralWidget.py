from gui.Box import HBox
from gui.TextEdit import TextEdit, make_label
from gui.code.widget_for import widget_for

from lib.observable.List import List

import style

class LiteralWidget(HBox):
    def __init__(self, literal, delimiter, escape_func):
        self.literal = literal
        self.delimiter = delimiter
        self.escape_func = escape_func
        s = style.literal_style_for[self.literal.__class__]
        HBox.__init__(self, List([
            make_label(s, delimiter),
            TextEdit(s, self._get_string, self._set_string, convertor=escape_func),
            make_label(s, delimiter),
        ]))

    def _get_string(self):
        return self.literal.value

    def _set_string(self, value):
        self.literal.value = value
