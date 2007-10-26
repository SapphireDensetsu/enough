# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from DefineWidget import DefineWidget
from IdentifierWidget import IdentifierWidget
import style

class DefineValueWidget(IdentifierWidget):
    def __init__(self, variable):
        IdentifierWidget.__init__(self, variable, style.define_value)
        self._info_widget = DefineWidget(self.variable)
