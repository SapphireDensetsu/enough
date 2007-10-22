from gui.Box import HBox
from gui.TextEdit import make_label
from gui.code.widget_for import widget_for

from observable.Join import Join
from observable.List import List
from observable.CacheMap import CacheMap

import style

class CallWidget(HBox):
    def __init__(self, call):
        self.call = call
        def make_comma():
            return make_label(style.comma, ', ')
        HBox.__init__(self, List([
            widget_for(self.call.func),
            make_label(style.paren, "("),
            HBox(Join(make_comma, CacheMap(widget_for, self.call.args))),
            make_label(style.paren, ")"),
        ]))
