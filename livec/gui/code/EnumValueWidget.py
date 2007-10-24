from InfoIdentifierWidget import InfoIdentifierWidget
from EnumWidget import EnumWidget
import style

class EnumValueWidget(InfoIdentifierWidget):
    def __init__(self, variable):
        InfoIdentifierWidget.__init__(self, variable, style.enum_value)
        self._type_widget = EnumWidget(self.variable.enum, self.variable)
