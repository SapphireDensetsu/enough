class Event(object):
    def __init__(self):
        self.handlers = {}

    def register(self, handler, key=None):
        if key is None:
            key = handler
        assert key not in self.handlers
        self.handlers[key] = handler
    def unregister(self, key):
        del self.handlers[key]

    def send(self, *args, **kw):
        for handler in self.handlers.itervalues():
            handled = handler(*args, **kw)
            if handled:
                break
