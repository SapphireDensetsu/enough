from IdentifierWidget import IdentifierWidget
from gui.loop import loop

class InfoIdentifierWidget(IdentifierWidget):
    def got_focus(self):
        IdentifierWidget.got_focus(self)
        loop.browser.info_stack.push(self._type_widget)
    def lost_focus(self):
        IdentifierWidget.lost_focus(self)
        loop.browser.info_stack.remove(self._type_widget)
