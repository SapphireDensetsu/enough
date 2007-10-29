# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import HBox
from gui.TextEdit import make_label
from codegui.widget_for import widget_for

from lib.observable.List import List

import style

class ReturnWidget(HBox):
    def __init__(self, return_proxy):
        self.return_ = return_proxy.get()

        HBox.__init__(self, List([
            make_label(style.return_, "return "),
            widget_for(self.return_.expr),
            make_label(style.semicolon, ";"),
        ]))
