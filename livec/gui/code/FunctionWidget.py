from gui.Box import VBox
from gui.TextEdit import TextEdit
#from gui.Label import Label
from gui.code import widget_for

class FunctionWidget(VBox):
    def __init__(self, function):
        self.function = function
        self.meta_widget = widget_for(self.function.meta)
        self.return_type_widget = widget_for(self.function.return_type)
        VBox.__init__(self, lambda : [self.meta_widget, self.return_type_widget])
