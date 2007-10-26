# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.TextEdit import TextEdit, TextStyle
from gui.loop import loop
from gui.Spacer import Spacer
from gui import Keymap
from InfoMixin import InfoMixin

import style

class IdentifierWidget(InfoMixin, TextEdit):
    def __init__(self, variable, var_style):
        self.variable = variable
        self.var_style = var_style
        self._info_widget = Spacer((0, 0))
        TextEdit.__init__(self, var_style,
                          self._get_name, self._set_name,
                          [Keymap.alphanumeric],
                          allowed_text=self._valid_identifier)

    def _get_name(self):
        return loop.namer.get_name(self.variable)

    def _set_name(self, name):
        self.variable.meta['name'] = name

    def _valid_identifier(self, name):
        return not name[:1].isdigit()
