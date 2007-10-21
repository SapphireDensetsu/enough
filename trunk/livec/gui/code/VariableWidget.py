from gui.Box import VBox, HBox
from gui.TextEdit import TextEdit
#from gui.Label import Label
from gui.code import widget_for

from List import List

class VariableWidget(HBox):
    def __init__(self, variable):
        self.variable = variable
        HBox.__init__(self, List([
            widget_for(self.variable.type),
            TextEdit(lambda : self.variable.meta['name']),
        ]))
        self.is_centered = True
