# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import HBox
from codegui.widget_for import posttype_widget_for, widget_for
from codegui import style

from lib.observable.List import List

class ArrayPostTypeWidget(HBox):
    def __init__(self, _type_proxy, variable_proxy):
        self.type = _type_proxy.get()

        HBox.__init__(self, List([
            make_label(style.paren, '('),
            posttype_widget_for(self.type.element_type, variable_proxy),
            make_label(style.bracket, '['),
            widget_for(self.type.size),
            make_label(style.bracket, ']'),
            make_label(style.paren, ')'),
        ]))
        self.is_centered = True
