from gui.Box import VBox, HBox
from gui.TextEdit import make_label
from gui.code.widget_for import widget_for, type_widget_for, declaration_widget_for, indented
from gui.code import style

from List import List
from CacheMap import CacheMap
        
class FunctionWidget(VBox):
    def __init__(self, function):
        self.function = function
        self.return_type_widget = type_widget_for(self.function.return_type)
        self.name_widget = make_label(self.function.meta['name'], color=style.func_name_color)
        
        self.parameters_widget = HBox(CacheMap(declaration_widget_for,
                                               self.function.parameters))
        self.parameters_widget.is_centered = True
        
        prototype = HBox(List([
            self.return_type_widget,
            self.name_widget,
            make_label('(', color=style.paren_color),
            self.parameters_widget,
            make_label(')', color=style.paren_color),
        ]))
        prototype.is_centered = True
        
        VBox.__init__(self, List([
            prototype,
            make_label('{', color=style.braces_color),
            indented(widget_for(self.function.block)),
            make_label('}', color=style.braces_color),
        ]))
