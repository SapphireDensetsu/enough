from gui.Box import VBox, HBox
from gui.TextEdit import TextEdit
#from gui.Label import Label
from gui.code import widget_for

from List import List

class VariableWidget(VBox):
    def __init__(self, variable):
        self.variable = variable
        VBox.__init__(self, List([
            TextEdit(lambda : self.variable.meta['name']),
#            widget_for(self.variable.type),
        ]))
