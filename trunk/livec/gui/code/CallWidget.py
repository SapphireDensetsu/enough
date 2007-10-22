from gui.Box import HBox
from gui.TextEdit import make_label
from gui.code.widget_for import widget_for

from List import List
from CacheMap import CacheMap

import style

class CallWidget(HBox):
    def __init__(self, call):
        self.call = call
        HBox.__init__(self, List([
            widget_for(self.call.func),
            make_label("(", color=style.paren_color),
            HBox(CacheMap(widget_for, self.call.args)),
            make_label(")", color=style.paren_color),
        ]))
