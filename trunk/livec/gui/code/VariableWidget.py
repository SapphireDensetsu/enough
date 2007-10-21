from gui.Box import VBox, HBox
from gui.TextEdit import TextEdit
#from gui.Label import Label
from gui.code import widget_for


class VariableWidget(VBox):
    def __init__(self, variable):
        self.variable = variable
        self.meta_widget = widget_for(self.variable.meta)
        self.meta_widget.draw_rect = False
        VBox.__init__(self, lambda : [self.meta_widget])
