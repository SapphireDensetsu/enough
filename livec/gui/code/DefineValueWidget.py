# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from InfoIdentifierWidget import InfoIdentifierWidget
from DefineWidget import DefineWidget
import style

class DefineValueWidget(InfoIdentifierWidget):
    def __init__(self, variable):
        InfoIdentifierWidget.__init__(self, variable, style.define_value)
        self._type_widget = DefineWidget(self.variable)
