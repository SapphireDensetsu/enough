from gui.Box import VBox, HBox
from gui.TextEdit import TextEdit
#from gui.Label import Label
from gui.code import widget_for, tabbed

from CacheMap import CacheMap
from List import List

def join(seq, mix_item):
    siter = iter(seq)
    for i in siter:
        yield i
        break
    else:
        return
    for i in siter:
        yield mix_item
        yield i
        
class FunctionWidget(VBox):
    def __init__(self, function):
        self.function = function
        self.return_type_widget = widget_for(self.function.return_type)
        self.name_widget = TextEdit(lambda : self.function.meta['name'])
        
        self.parameters_widget = HBox(CacheMap(widget_for,
                                               join(self.function.parameters, ',')))
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
            widget_for('{'),
            tabbed(self.block_widget),
            widget_for('}'),
        ]))
