# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from IdentifierWidget import IdentifierWidget
from gui.loop import loop

class InfoIdentifierWidget(IdentifierWidget):
    def got_focus(self):
        IdentifierWidget.got_focus(self)
        loop.browser.add_info_widget(self._type_widget)
    def lost_focus(self):
        IdentifierWidget.lost_focus(self)
        loop.browser.remove_info_widget(self._type_widget)
