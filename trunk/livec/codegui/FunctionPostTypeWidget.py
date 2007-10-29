# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import HBox
from gui.TextEdit import make_label
from codegui.widget_for import posttype_widget_for, declaration_widget_for
from codegui import style

from lib.observable.List import List
from lib.observable.CacheMap import CacheMap
        
class FunctionPostTypeWidget(HBox):
    is_centered = True
    def __init__(self, function_type_proxy, variable_proxy):
        self.function_type = function_type_proxy.get()

        comma = make_label(style.comma, ', ')
        
        self.parameters_widget = HBox(CacheMap(declaration_widget_for,
                                               self.function_type.parameters))
        self.parameters_widget.padding_widget = comma
        self.parameters_widget.is_centered = True

        HBox.__init__(self, List([
            posttype_widget_for(self.function_type.return_type, variable_proxy),
            make_label(style.paren, '('),
            self.parameters_widget,
            make_label(style.paren, ')'),
        ]))
