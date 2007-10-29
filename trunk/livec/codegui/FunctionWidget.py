# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import VBox, HBox
from gui.TextEdit import make_label
from codegui.widget_for import NormalWidgetMaker, TypeWidgetMaker

from lib.observable.List import List
        
class FunctionWidget(VBox):
    def __init__(self, function_proxy):
        self.function_proxy = function_proxy
        self.function = function_proxy.get()

        VBox.__init__(self, List([
            TypeWidgetMaker.make(self.function.type, self.function_proxy),
            NormalWidgetMaker.make(self.function.block),
        ]))
