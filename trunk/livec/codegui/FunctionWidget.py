# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import VBox, HBox
from gui.TextEdit import make_label
from codegui.widget_for import widget_for, type_widget_for, declaration_widget_for

from lib.observable.List import List
        
class FunctionWidget(VBox):
    def __init__(self, function_proxy):
        self.function_proxy = function_proxy
        self.function = function_proxy.get()

        VBox.__init__(self, List([
            self._widget_for_prototype(self.function.type),
            widget_for(self.function.block),
        ]))

    def _widget_for_prototype(self, type_):
        return type_widget_for(type_, self.function_proxy)
