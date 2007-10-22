from styletools import StyledTextEdit
from gui.code.widget_for import widget_for

from observable.List import List

import style

class LiteralWidget(StyledTextEdit):
    def __init__(self, literal, value_string):
        self.literal = literal
        color = style.literal_color_for[self.literal.__class__]
        StyledTextEdit.__init__(self, lambda : value_string(self.literal.value),
                          color=color)
