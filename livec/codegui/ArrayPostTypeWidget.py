# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import HBox
from codegui.widget_for import posttype_widget_for, widget_for
from codegui import style
from gui.ProxyWidget import ProxyWidget

from lib.observable.List import List
from lib.observable.DictOfAttrs import DictOfAttrs
from lib.DictProxy import DictProxy

class ArrayPostTypeWidget(HBox):
    def __init__(self, _type, variable):
        self.type = _type

        d = DictProxy(DictOfAttrs(self.type))

        HBox.__init__(self, List([
            make_label(style.paren, '('),
            posttype_widget_for(self.type.element_type, variable),
            make_label(style.bracket, '['),
            ProxyWidget(d.map('size', widget_for)),
            make_label(style.bracket, ']'),
            make_label(style.paren, ')'),
        ]))
        self.is_centered = True
