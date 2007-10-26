# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import VBox, HBox
from widget_for import type_widget_for
from gui.ProxyWidget import ProxyWidget

from lib.DictMap import DictMap
from lib.observable.List import List
from lib.observable.DictOfAttrs import DictOfAttrs

class VariableDeclarationWidget(HBox):
    is_centered = True
    def __init__(self, variable):
        self.variable = variable

        d = DictMap(DictOfAttrs(self.variable))

        HBox.__init__(self, List([
            ProxyWidget(d.map('type', self._widget_for_type)),
        ]))

    def _widget_for_type(self, typ):
        return type_widget_for(typ, self.variable)
