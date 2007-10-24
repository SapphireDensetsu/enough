from gui.Box import HBox
from gui.TextEdit import TextEdit, make_label
from gui.code.widget_for import widget_for
from gui import Keymap

from lib.observable.List import List

import style

class LiteralWidget(HBox):
    def __init__(self, literal, delimiter, escape_table):
        self.literal = literal
        self.delimiter = delimiter
        self.escape_table = escape_table.copy()
        self.escape_table['\r'] = '\\n'
        s = style.literal_style_for[self.literal.__class__]
        HBox.__init__(self, List([
            make_label(s, delimiter),
            TextEdit(s, self._get_string, self._set_string,
                     [Keymap.alphanumeric, Keymap.text_control],
                     convertor=self.escape_table),
            make_label(s, delimiter),
        ]))

    def _get_string(self):
        return self.literal.value

    def _set_string(self, value):
        self.literal.value = value
