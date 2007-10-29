# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import HBox
from gui.TextEdit import make_label
from codegui.widget_for import NormalWidgetMaker

from lib.observable.List import List
from lib.observable.CacheMap import CacheMap

import style

class CallWidget(HBox):
    def __init__(self, call_proxy):
        self.call = call_proxy.get()

        comma = make_label(style.comma, ', ')
        args_box = HBox(CacheMap(NormalWidgetMaker.make, self.call.args), relay_focus=True)
        args_box.padding_widget = comma
        HBox.__init__(self, List([
            NormalWidgetMaker.make(self.call.func),
            make_label(style.paren, "("),
            args_box,
            make_label(style.paren, ")"),
        ]))
import nodes
NormalWidgetMaker.register(nodes.Call, CallWidget)
