# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from IdentifierWidget import IdentifierWidget
from VariableDeclarationWidget import VariableDeclarationWidget
import style

class VariableWidget(IdentifierWidget):
    def __init__(self, variable_proxy):
        IdentifierWidget.__init__(self, variable_proxy, style.variable_name)
        self._info_shower.info_widget = VariableDeclarationWidget(variable_proxy)
import nodes
from widget_for import NormalWidgetMaker
NormalWidgetMaker.register(nodes.Variable, VariableWidget)
