# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import HBox
from gui.ProxyWidget import ProxyWidget
from gui.TextEdit import make_label
from gui.loop import loop
from gui.code.widget_for import widget_for, indented
import style

from lib.observable.List import List
from lib.observable.DictOfAttrs import DictOfAttrs

from lib.DictMap import DictMap

class DefineWidget(HBox):
    def __init__(self, define):
        self.define = define

        d = DictMap(DictOfAttrs(self.define))
        HBox.__init__(self, List([
            make_label(style.define, '#define'),
            make_label(style.space, ' '),
            make_label(style.define_value, loop.namer.get_name(self.define)),
            make_label(style.space, ' '),
            ProxyWidget(d.map('expr', widget_for)),
        ]), relay_focus=True)
