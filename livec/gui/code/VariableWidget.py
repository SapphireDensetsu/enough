from gui.Box import VBox, HBox
from gui.TextEdit import TextEdit
#from gui.Label import Label
from gui.code import widget_for


class VariableWidget(VBox):
    def __init__(self, variable):
        self.variable = variable
        self.meta_widget = widget_for(self.variable.meta)
        VBox.__init__(self)
        self.add_child(self.meta_widget)
