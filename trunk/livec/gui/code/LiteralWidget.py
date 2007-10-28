# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import HBox
from gui.TextEdit import TextEdit, make_label
from gui import Keymap
from InfoShower import InfoShower

from lib.observable.List import List

class LiteralWidget(HBox):
    example_frame_color = None
    def __init__(self, literal):
        self.literal = literal
        self.text_edit = TextEdit(self.literal_style,
                                  self._get_string, self._set_string,
                                  [Keymap.all_printable],
                                  convertor=self.escape_table,
                                  allowed_text=self._allowed_text)
        example = TextEdit(self.example_style, self._get_example_str)
        example.frame_color = self.example_frame_color
        HBox.__init__(self, List([
            make_label(self.delimiter_style, self.delimiter),
            self.text_edit,
            make_label(self.delimiter_style, self.delimiter),
        ]), relay_focus=True)
        self._info_shower = InfoShower(self.text_edit.focus_keymap.obs_activation)
        self._info_shower.info_widget = example

    def _get_string(self):
        return self._string_of_value(self.literal.value)

    def _set_string(self, value):
        self.literal.value = self._value_of_string(value)

    def _string_of_value(self, value):
        return value

    def _value_of_string(self, value):
        return value.replace('\r', '\n')

    def _allowed_text(self, value):
        return True
