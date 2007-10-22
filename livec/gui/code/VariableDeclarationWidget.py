from gui.Box import VBox, HBox
from gui.TextEdit import make_label
from gui.code.widget_for import type_widget_for, style

from observable.List import List

class VariableDeclarationWidget(HBox):
    is_centered = True
    def __init__(self, variable):
        self.variable = variable
        name = self.variable.meta.get('name', '<noname>')
        HBox.__init__(self, List([
            type_widget_for(self.variable.type, name),
        ]))
