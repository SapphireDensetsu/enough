from gui.Box import HBox
from gui.TextEdit import make_label
from gui.code.widget_for import widget_for

from observable.List import List
from observable.CacheMap import CacheMap

import style

class CallWidget(HBox):
    def __init__(self, call):
        self.call = call
        comma = make_label(style.comma, ', ')
        args_box = HBox(CacheMap(widget_for, self.call.args))
        args_box.padding_widget = comma
        HBox.__init__(self, List([
            widget_for(self.call.func),
            make_label(style.paren, "("),
            args_box,
            make_label(style.paren, ")"),
        ]))
