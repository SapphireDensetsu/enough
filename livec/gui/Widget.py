from Keymap import Keymap

class Widget(object):
    def __init__(self):
        self.keymap = Keymap()
    def draw(self, surface, pos):
        raise NotImplementedError()
    def size(self):
        raise NotImplementedError()
