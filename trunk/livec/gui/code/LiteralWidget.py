from gui.TextEdit import TextEdit
from gui.code.widget_for import widget_for

from observable.List import List

import style

class LiteralWidget(TextEdit):
    def __init__(self, literal, value_string):
        self.literal = literal
        color = style.literal_color_for[self.literal.__class__]
        TextEdit.__init__(self, lambda : value_string(self.literal.value),
                          color=color)
