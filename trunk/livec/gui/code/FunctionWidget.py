from gui.Box import VBox, HBox
from gui.TextEdit import TextEdit
#from gui.Label import Label
from gui.code import widget_for

from CacheMap import CacheMap
from List import List

def mix(a,mix_item):
    for i in a[:-1]:
        yield i
        yield mix_item
    yield a[-1]
        
class FunctionWidget(VBox):
    def __init__(self, function):
        self.function = function
        self.return_type_widget = widget_for(self.function.return_type)
        self.name_widget = TextEdit(lambda : self.function.meta['name'])
        
        self.parameters_widget = HBox(CacheMap(widget_for,
                                               mix(self.function.parameters, ',')))
        self.parameters_widget.is_centered = True
        
        self.block_widget = widget_for(self.function.block)
        prototype = HBox(List([
            self.return_type_widget,
            self.name_widget,
            TextEdit(lambda : '('),
            self.parameters_widget,
            TextEdit(lambda : ')'),
        ]))
        prototype.is_centered = True
        VBox.__init__(self, List([
            prototype,
            self.block_widget
        ]))
