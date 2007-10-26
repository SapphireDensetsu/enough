# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import HBox
from gui.TextEdit import make_label
from gui.code.widget_for import widget_for
from gui.ProxyWidget import ProxyWidget

from lib.observable.List import List
from lib.observable.DictOfAttrs import DictOfAttrs
from lib.DictMap import DictMap

import style

class ReturnWidget(HBox):
    def __init__(self, return_):
        self.return_ = return_

        d = DictMap(DictOfAttrs(self.return_))

        HBox.__init__(self, List([
            make_label(style.return_, "return "),
            ProxyWidget(d.map('expr', widget_for)),
            make_label(style.semicolon, ";"),
        ]))
