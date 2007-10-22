from styletools import styled_label
from gui.Box import HBox
from gui.code.widget_for import posttype_widget_for
from gui.code import style

from observable.List import List

class PtrTypeWidget(HBox):
    def __init__(self, _type, name):
        self.type = _type
        HBox.__init__(self, List([
            styled_label('(', color=style.paren_color),
            styled_label('*', color=style.type_color),
            posttype_widget_for(self.type.pointed_type, name),
            styled_label(')', color=style.paren_color),
        ]))
        self.is_centered = True
