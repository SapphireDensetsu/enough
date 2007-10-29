# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import VBox, HBox
from widget_for import type_widget_for

from lib.observable.List import List

class VariableDeclarationWidget(HBox):
    is_centered = True
    def __init__(self, variable_proxy):
        self.variable_proxy = variable_proxy
        self.variable = variable_proxy.get()

        HBox.__init__(self, List([
            self._widget_for_type(self.variable.type),
        ]))

    def _widget_for_type(self, typ):
        return type_widget_for(typ, self.variable_proxy)
