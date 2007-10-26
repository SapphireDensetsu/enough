# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from InfoIdentifierWidget import InfoIdentifierWidget
from EnumWidget import EnumWidget
import style
from gui.ProxyWidget import ProxyWidget

from lib.observable.DictOfAttrs import DictOfAttrs
from lib.DictMap import DictMap

class EnumValueWidget(InfoIdentifierWidget):
    def __init__(self, variable):
        InfoIdentifierWidget.__init__(self, variable, style.enum_value)

        d = DictMap(DictOfAttrs(self.variable))

        self._type_widget = ProxyWidget(d.map('enum', self._widget_for))

    def _widget_for(self, enum):
        return EnumWidget(enum, self.variable)
