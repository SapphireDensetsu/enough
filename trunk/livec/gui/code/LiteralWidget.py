from gui.TextEdit import TextEdit
from gui.code.widget_for import widget_for

from observable.List import List

import style

class LiteralWidget(TextEdit):
    def __init__(self, literal, value_string):
        self.literal = literal
        s = style.literal_style_for[self.literal.__class__]
        TextEdit.__init__(self, s, lambda : value_string(self.literal.value))
