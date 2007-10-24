from IdentifierWidget import IdentifierWidget
import style
from gui.loop import loop
from VariableDeclarationWidget import VariableDeclarationWidget

class VariableWidget(IdentifierWidget):
    def __init__(self, variable):
        IdentifierWidget.__init__(self, variable, style.variable_name)
        self._type_widget = VariableDeclarationWidget(self.variable)
    def got_focus(self):
        IdentifierWidget.got_focus(self)
        loop.browser.info_stack.push(self._type_widget)
    def lost_focus(self):
        IdentifierWidget.lost_focus(self)
        loop.browser.info_stack.remove(self._type_widget)
