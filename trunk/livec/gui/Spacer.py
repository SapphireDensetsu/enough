from gui.Widget import Widget

class Spacer(Widget):
    selectable = False
    def __init__(self, size):
        Widget.__init__(self)
        self._size = size
    def _draw(self, surface, pos):
        pass
    def size(self):
        return self._size
