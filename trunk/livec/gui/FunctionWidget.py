# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import VBox, HBox
from gui.ProxyWidget import ProxyWidget
from gui.TextEdit import make_label
from codegui.widget_for import widget_for, type_widget_for, declaration_widget_for

from lib.observable.List import List
from lib.observable.DictOfAttrs import DictOfAttrs
from lib.DictMap import DictMap
        
class FunctionWidget(VBox):
    def __init__(self, function):
        self.function = function

        d = DictMap(DictOfAttrs(self.function))

        VBox.__init__(self, List([
            ProxyWidget(d.map('type', self._widget_for_prototype)),
            ProxyWidget(d.map('block', widget_for)),
        ]))

    def _widget_for_prototype(self, typ):
        return type_widget_for(typ, self.function)
