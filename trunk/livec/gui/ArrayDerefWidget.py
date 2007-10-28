# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import HBox
from gui.TextEdit import make_label
from codegui.widget_for import widget_for
from gui.ProxyWidget import ProxyWidget

from lib.observable.List import List
from lib.observable.DictOfAttrs import DictOfAttrs
from lib.DictMap import DictMap

import style

class ArrayDerefWidget(HBox):
    def __init__(self, array_deref):
        self.array_deref = array_deref

        d = DictMap(DictOfAttrs(self.array_deref))

        HBox.__init__(self, List([
            ProxyWidget(d.map('expr', widget_for)),
            make_label(style.bracket, "["),
            ProxyWidget(d.map('index', widget_for)),
            make_label(style.bracket, "]"),
        ]))
