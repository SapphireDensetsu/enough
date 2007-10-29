# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from IdentifierWidget import IdentifierWidget
from EnumWidget import EnumWidget
import style

class EnumValueWidget(IdentifierWidget):
    def __init__(self, variable_proxy):
        IdentifierWidget.__init__(self, variable_proxy, style.enum_value)

        self._info_shower.info_widget = self._widget_for(self.variable.enum)

    def _widget_for(self, enum_proxy):
        return EnumWidget(enum_proxy, self.variable)
