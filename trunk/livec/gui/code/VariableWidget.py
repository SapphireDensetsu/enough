from gui.TextEdit import TextEdit
from gui.code.widget_for import widget_for

from List import List

class VariableWidget(TextEdit):
    def __init__(self, variable):
        self.variable = variable
        TextEdit.__init__(self, (lambda : self.variable.meta.get('name', '<noname>')))
