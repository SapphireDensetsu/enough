# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.TextEdit import make_label
from gui.Box import HBox
from gui.code.widget_for import posttype_widget_for
from gui.code import style

from lib.observable.List import List

class PtrTypeWidget(HBox):
    def __init__(self, _type, variable):
        self.type = _type
        HBox.__init__(self, List([
            make_label(style.paren, '('),
            make_label(style.type_, '*'),
            posttype_widget_for(self.type.pointed_type, variable),
            make_label(style.paren, ')'),
        ]))
        self.is_centered = True
