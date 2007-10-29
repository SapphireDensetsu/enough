# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.TextEdit import make_label
from gui.Box import HBox
from codegui.widget_for import PostTypeWidgetMaker
from codegui import style

from lib.observable.List import List

class PtrPostTypeWidget(HBox):
    def __init__(self, _type_proxy, variable_proxy):
        self.type = _type_proxy.get()
        HBox.__init__(self, List([
            make_label(style.paren, '('),
            make_label(style.type_, '*'),
            PostTypeWidgetMaker.make(self.type.pointed_type, variable_proxy),
            make_label(style.paren, ')'),
        ]))
        self.is_centered = True
import nodes
PostTypeWidgetMaker.register(nodes.Ptr, PtrPostTypeWidget)
