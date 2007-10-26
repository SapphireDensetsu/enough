# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import HBox
from gui.TextEdit import TextEdit, make_label
from gui.code.widget_for import widget_for
from gui.loop import loop
from gui import Keymap

from lib.observable.List import List

import style

class _LiteralTextEdit(TextEdit):
    def got_focus(self):
        TextEdit.got_focus(self)
        loop.browser.add_info_widget(self._string_widget)

    def lost_focus(self):
        TextEdit.lost_focus(self)
        loop.browser.remove_info_widget(self._string_widget)

class LiteralWidget(HBox):
    def __init__(self, literal, delimiter, escape_table):
        self.literal = literal
        self.delimiter = delimiter
        self.escape_table = escape_table
        s = style.literal_style_for[self.literal.__class__]
        text_edit = _LiteralTextEdit(s, self._get_string, self._set_string,
                                     [Keymap.all_printable],
                                     convertor=self.escape_table)
        text_edit._string_widget = TextEdit(s, self._get_string)
        HBox.__init__(self, List([
            make_label(s, delimiter),
            text_edit,
            make_label(s, delimiter),
        ]), relay_focus=True)

    def _get_string(self):
        return self.literal.value

    def _set_string(self, value):
        self.literal.value = value.replace('\r', '\n')
