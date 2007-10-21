from gui.Box import VBox, HBox
from gui.TextEdit import TextEdit
#from gui.Label import Label
from gui.code import widget_for

from CacheMap import CacheMap
from List import List

class FunctionWidget(VBox):
    def __init__(self, function):
        self.function = function
        self.meta_widget = widget_for(self.function.meta)
        self.return_type_widget = widget_for(self.function.return_type)
        self.name_widget = TextEdit(lambda : self.function.meta['name'])
        self.parameters_widget = HBox(CacheMap(widget_for, self.function.parameters))
        
        self.block_widget = widget_for(self.function.block)
        VBox.__init__(self, List([
            self.meta_widget,
            HBox(List([
                self.return_type_widget,
                self.name_widget,
                self.parameters_widget,
            ])),
            self.block_widget
        ]))
