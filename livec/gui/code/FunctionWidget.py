from gui.Box import VBox, HBox
from gui.TextEdit import make_label
from gui.code.widget_for import widget_for, type_widget_for, declaration_widget_for, indented
from gui.code import style

from observable.List import List
from observable.CacheMap import CacheMap
from observable.Join import Join
        
class FunctionWidget(VBox):
    def __init__(self, function):
        self.function = function
        self.return_type_widget = type_widget_for(self.function.return_type)
        self.name_widget = make_label(style.func_name, self.function.meta['name'])

        def make_comma():
            return make_label(style.comma, ', ')
        
        self.parameters_widget = HBox(Join(make_comma,
                                           CacheMap(declaration_widget_for,
                                                    self.function.parameters)))
        self.parameters_widget.is_centered = True
        
        prototype = HBox(List([
            self.return_type_widget,
            make_label(style.default, ' '),
            self.name_widget,
            make_label(style.paren, '('),
            self.parameters_widget,
            make_label(style.paren, ')'),
        ]))
        prototype.is_centered = True
        
        VBox.__init__(self, List([
            prototype,
            make_label(style.braces, '{'),
            indented(widget_for(self.function.block)),
            make_label(style.braces, '}'),
        ]))
