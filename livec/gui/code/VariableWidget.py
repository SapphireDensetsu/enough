# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from IdentifierWidget import IdentifierWidget
import style
from VariableDeclarationWidget import VariableDeclarationWidget

class VariableWidget(IdentifierWidget):
    def __init__(self, variable):
        IdentifierWidget.__init__(self, variable, style.variable_name)
        self._info_widget = VariableDeclarationWidget(self.variable)
