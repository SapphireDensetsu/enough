# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.TextEdit import TextEdit, TextStyle
from gui.loop import loop
from gui import Keymap
from InfoShower import InfoShower

import style

class IdentifierWidget(TextEdit):
    def __init__(self, variable, var_style):
        self.variable = variable
        self.var_style = var_style
        TextEdit.__init__(self, var_style,
                          self._get_name, self._set_name,
                          [Keymap.alphanumeric],
                          allowed_text=self._valid_identifier)
        self._info_shower = InfoShower(self.focus_keymap.obs_activation)

    def _get_name(self):
        return loop.namer.get_name(self.variable)

    def _set_name(self, name):
        self.variable.meta['name'] = name

    def _valid_identifier(self, name):
        return not name[:1].isdigit()
