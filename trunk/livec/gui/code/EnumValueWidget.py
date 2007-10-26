# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from IdentifierWidget import IdentifierWidget
from EnumWidget import EnumWidget
import style
from gui.ProxyWidget import ProxyWidget

from lib.observable.DictOfAttrs import DictOfAttrs
from lib.DictMap import DictMap

class EnumValueWidget(IdentifierWidget):
    def __init__(self, variable):
        IdentifierWidget.__init__(self, variable, style.enum_value)

        d = DictMap(DictOfAttrs(self.variable))

        self._info_widget = ProxyWidget(d.map('enum', self._widget_for))

    def _widget_for(self, enum):
        return EnumWidget(enum, self.variable)
