class Keymap(object):
    def __init__(self):
        self.keys = {}
    def keydown(self, event):
        if event.key not in self.keys:
            return False
        handler = self.keys[event.key]
        handler(event)
