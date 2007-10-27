# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Widget import Widget

class SpacerWidget(Widget):
    def __init__(self, size):
        Widget.__init__(self)
        self.selectable.set(False)
        self.size = size
    def _draw(self, surface, pos):
        pass
    def update(self):
        pass
