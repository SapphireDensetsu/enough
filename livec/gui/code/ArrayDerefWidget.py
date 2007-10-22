from gui.Box import HBox
from styletools import styled_label
from gui.code.widget_for import widget_for

from observable.List import List

import style

class ArrayDerefWidget(HBox):
    def __init__(self, array_deref):
        self.array_deref = array_deref
        HBox.__init__(self, List([
            widget_for(self.array_deref.expr),
            styled_label("[", color=style.bracket_color),
            widget_for(self.array_deref.index),
            styled_label("]", color=style.bracket_color),
        ]))
