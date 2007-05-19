from weakref import WeakValueDictionary
class WeakCollection(object):
    def __init__(self, seq=tuple()):
        self._d = WeakValueDictionary()
        for item in seq:
            self.add(item)
    def add(self, item):
        self._d[id(item)] = item
    def remove(self, item):
        del self._id[id(item)]
        
