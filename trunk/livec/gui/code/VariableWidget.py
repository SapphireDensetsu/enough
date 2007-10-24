from InfoIdentifierWidget import InfoIdentifierWidget
import style
from VariableDeclarationWidget import VariableDeclarationWidget

class VariableWidget(InfoIdentifierWidget):
    def __init__(self, variable):
        InfoIdentifierWidget.__init__(self, variable, style.variable_name)
        self._type_widget = VariableDeclarationWidget(self.variable)
