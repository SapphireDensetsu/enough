from gui.TextEdit import make_label
from gui.Box import HBox
from gui.code.widget_for import posttype_widget_for, widget_for
from gui.code import style

from observable.List import List

class ArrayTypeWidget(HBox):
    def __init__(self, _type, name):
        self.type = _type
        HBox.__init__(self, List([
            make_label('(', color=style.paren_color),
            posttype_widget_for(self.type.element_type, name),
            make_label('[', color=style.bracket_color),
            widget_for(self.type.size),
            make_label(']', color=style.bracket_color),
            make_label(')', color=style.paren_color),
        ]))
        self.is_centered = True
