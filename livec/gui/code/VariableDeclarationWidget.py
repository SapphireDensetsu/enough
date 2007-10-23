from gui.Box import VBox, HBox
from gui.code.widget_for import type_widget_for, style

from observable.List import List

class VariableDeclarationWidget(HBox):
    is_centered = True
    def __init__(self, variable):
        self.variable = variable
        HBox.__init__(self, List([
            type_widget_for(self.variable.type, self.variable),
        ]))
