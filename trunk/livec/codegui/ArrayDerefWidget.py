# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import HBox
from gui.TextEdit import make_label
from codegui.widget_for import widget_for

from lib.observable.List import List

import style

class ArrayDerefWidget(HBox):
    def __init__(self, array_deref_proxy):
        self.array_deref = array_deref_proxy.get()

        HBox.__init__(self, List([
            widget_for(self.array_deref.expr),
            make_label(style.bracket, "["),
            widget_for(self.array_deref.index),
            make_label(style.bracket, "]"),
        ]))
