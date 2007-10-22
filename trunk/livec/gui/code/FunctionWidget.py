from gui.Box import VBox, HBox
from styletools import styled_label
from gui.code.widget_for import widget_for, type_widget_for, declaration_widget_for, indented
from gui.code import style

from observable.List import List
from observable.CacheMap import CacheMap
from observable.Join import Join
        
class FunctionWidget(VBox):
    def __init__(self, function):
        self.function = function
        self.return_type_widget = type_widget_for(self.function.return_type)
        self.name_widget = styled_label(self.function.meta['name'], color=style.func_name_color)

        def make_comma():
            return styled_label(', ')
        
        self.parameters_widget = HBox(Join(make_comma,
                                           CacheMap(declaration_widget_for,
                                                    self.function.parameters)))
        self.parameters_widget.is_centered = True
        
        prototype = HBox(List([
            self.return_type_widget,
            styled_label(' '),
            self.name_widget,
            styled_label('(', color=style.paren_color),
            self.parameters_widget,
            styled_label(')', color=style.paren_color),
        ]))
        prototype.is_centered = True
        
        VBox.__init__(self, List([
            prototype,
            styled_label('{', color=style.braces_color),
            indented(widget_for(self.function.block)),
            styled_label('}', color=style.braces_color),
        ]))
