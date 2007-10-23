from gui.Box import HBox
from gui.code.widget_for import posttype_widget_for, widget_for
from gui.code import style

from observable.List import List

class ArrayTypeWidget(HBox):
    def __init__(self, _type, variable):
        self.type = _type
        HBox.__init__(self, List([
            make_label(style.paren, '('),
            posttype_widget_for(self.type.element_type, variable),
            make_label(style.bracket, '['),
            widget_for(self.type.size),
            make_label(style.bracket, ']'),
            make_label(style.paren, ')'),
        ]))
        self.is_centered = True
