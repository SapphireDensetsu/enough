# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import VBox, HBox
from widget_for import TypeWidgetMaker, DeclarationWidgetMaker

from lib.observable.List import List

class VariableDeclarationWidget(HBox):
    is_centered = True
    def __init__(self, variable_proxy):
        self.variable_proxy = variable_proxy
        self.variable = variable_proxy.get()

        HBox.__init__(self, List([
            TypeWidgetMaker.make(self.variable.type, self.variable_proxy),
        ]))
import nodes
DeclarationWidgetMaker.register(nodes.Variable, VariableDeclarationWidget)
