from gui.Widget import Widget

class Spacer(Widget):
    def __init__(self, size):
        self._size = size
    def draw(self, surface, pos):
        pass
    def size(self):
        return self._size
