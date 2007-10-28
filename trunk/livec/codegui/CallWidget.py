# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import HBox
from gui.TextEdit import make_label
from codegui.widget_for import widget_for
from gui.ProxyWidget import ProxyWidget

from lib.observable.List import List
from lib.observable.CacheMap import CacheMap
from lib.observable.DictOfAttrs import DictOfAttrs
from lib.DictProxy import DictProxy

import style

class CallWidget(HBox):
    def __init__(self, call):
        self.call = call

        d = DictProxy(DictOfAttrs(self.call))

        comma = make_label(style.comma, ', ')
        args_box = HBox(CacheMap(widget_for, self.call.args), relay_focus=True)
        args_box.padding_widget = comma
        HBox.__init__(self, List([
            ProxyWidget(d.map('func', widget_for)),
            make_label(style.paren, "("),
            args_box,
            make_label(style.paren, ")"),
        ]))
