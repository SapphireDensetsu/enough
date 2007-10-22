from gui.Box import HBox
from gui.TextEdit import make_label
from gui.code.widget_for import widget_for

from List import List

import style

class ReturnWidget(HBox):
    def __init__(self, return_):
        self.return_ = return_
        HBox.__init__(self, List([
            make_label("return", color=style.return_color),
            widget_for(self.return_.expr)
        ]))
