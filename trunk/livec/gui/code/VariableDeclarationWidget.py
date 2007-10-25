# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import VBox, HBox
from widget_for import type_widget_for

from lib.observable.List import List

class VariableDeclarationWidget(HBox):
    is_centered = True
    def __init__(self, variable):
        self.variable = variable
        HBox.__init__(self, List([
            type_widget_for(self.variable.type, self.variable),
        ]))
