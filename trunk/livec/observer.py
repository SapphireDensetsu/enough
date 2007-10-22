# TODO: When do we remove_observer? Use weakref?
class Observable(object):
    def __init__(self):
        self.observers = []
    def add_observer(self, observer):
        self.observers.append(observer)
    def remove_observer(self, observer):
        self.observers.remove(observer)
