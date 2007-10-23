from gui.Box import VBox, HBox
from gui.TextEdit import make_label
from gui.code.widget_for import widget_for, type_widget_for, declaration_widget_for, indented
from gui.code import style

from lib.observable.List import List
        
class FunctionWidget(VBox):
    def __init__(self, function):
        self.function = function
        self.prototype_widget = type_widget_for(self.function.type, self.function)
        
        VBox.__init__(self, List([
            self.prototype_widget,
            make_label(style.braces, '{'),
            indented(widget_for(self.function.block)),
            make_label(style.braces, '}'),
        ]))
