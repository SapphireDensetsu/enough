# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from DefineWidget import DefineWidget
from IdentifierWidget import IdentifierWidget
import style

class DefineValueWidget(IdentifierWidget):
    def __init__(self, variable_proxy):
        IdentifierWidget.__init__(self, variable_proxy, style.define_value)
        self._info_shower.info_widget = DefineWidget(variable_proxy)
import nodes
from widget_for import NormalWidgetMaker
NormalWidgetMaker.register(nodes.Define, DefineValueWidget)
