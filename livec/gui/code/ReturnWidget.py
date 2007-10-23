from gui.Box import HBox
from gui.TextEdit import make_label
from gui.code.widget_for import widget_for

from observable.List import List

import style

class ReturnWidget(HBox):
    def __init__(self, return_):
        self.return_ = return_
        HBox.__init__(self, List([
            make_label(style.return_, "return "),
            widget_for(self.return_.expr)
        ]))
