# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import HBox
from gui.TextEdit import TextEdit, make_label
from codegui.loop import loop
from codegui.widget_for import NormalWidgetMaker, DeclarationWidgetMaker, indented
import style

from lib.observable.List import List

from functools import partial

class DefineWidget(HBox):
    def __init__(self, define_proxy):
        self.define = define_proxy.get()

        HBox.__init__(self, List([
            make_label(style.define, '#define'),
            make_label(style.space, ' '),
            TextEdit(style.define_value, partial(loop.namer.get_name, self.define)),
            make_label(style.space, ' '),
            NormalWidgetMaker.make(self.define.expr),
        ]), relay_focus=True)
import nodes
DeclarationWidgetMaker.register(nodes.Define, DefineWidget)
