from gui.TextEdit import TextEdit
from gui.loop import loop
from gui.TextEdit import TextStyle

import style

class IdentifierWidget(TextEdit):
    def __init__(self, variable, s):
        self.variable = variable
        if 'name' in self.variable.meta:
            name = self.variable.meta['name']
        else:
            name = loop.browser.get_name(self.variable)
            s = TextStyle.from_style(s)
            s.bgcolor = style.unnamed_bg_color
        TextEdit.__init__(self, s, (lambda : name))
