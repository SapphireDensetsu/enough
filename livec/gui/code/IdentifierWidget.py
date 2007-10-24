from gui.TextEdit import TextEdit, TextStyle
from gui.loop import loop
from gui import Keymap

import style

class IdentifierWidget(TextEdit):
    def __init__(self, variable, var_style):
        self.variable = variable
        self.var_style = var_style
        TextEdit.__init__(self, var_style, self._get_name, self._set_name,
                          [Keymap.alphanumeric])

    def _get_name(self):
        if 'name' in self.variable.meta:
            return self.variable.meta['name']
        else:
            return loop.browser.get_name(self.variable)

    def _set_name(self, name):
        if name[0].isdigit():
            return
        self.variable.meta['name'] = name
