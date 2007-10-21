from gui.Box import VBox, HBox
from gui.TextEdit import TextEdit
#from gui.Label import Label
from gui.code import widget_for


class FunctionWidget(VBox):
    def __init__(self, function):
        self.function = function
        self.meta_widget = widget_for(self.function.meta)
        self.return_type_widget = widget_for(self.function.return_type)
        self.name_widget = TextEdit(lambda : self.function.meta['name'])
        self.parameters_widget = HBox()
        for param in self.function.parameters:
            self.parameters_widget.add_child(widget_for(param))
        
        self.block_widget = widget_for(self.function.block)
        VBox.__init__(self)
        self.add_child(self.meta_widget)
        h = HBox()
        h.add_child(self.return_type_widget)
        h.add_child(self.name_widget)
        h.add_child(self.parameters_widget)
        self.add_child(h)
        self.add_child(self.block_widget)
