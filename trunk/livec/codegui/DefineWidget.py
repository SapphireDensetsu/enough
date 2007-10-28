# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import HBox
from gui.ProxyWidget import ProxyWidget
from gui.TextEdit import TextEdit, make_label
from codegui.loop import loop
from codegui.widget_for import widget_for, indented
import style

from lib.observable.List import List
from lib.observable.DictOfAttrs import DictOfAttrs

from lib.DictProxy import DictProxy

from functools import partial

class DefineWidget(HBox):
    def __init__(self, define):
        self.define = define

        d = DictProxy(DictOfAttrs(self.define))
        HBox.__init__(self, List([
            make_label(style.define, '#define'),
            make_label(style.space, ' '),
            TextEdit(style.define_value, partial(loop.namer.get_name, self.define)),
            make_label(style.space, ' '),
            ProxyWidget(d.map('expr', widget_for)),
        ]), relay_focus=True)
