from observer import Observable

class List(Observable):
    def __init__(self, *args, **kw):
        Observable.__init__(self)
        self._items = list(*args, **kw)

    def insert(self, index, item):
        self._items.insert(index, item)
        for observer in self.observers:
            observer.observe_insert(self, index, item)
    
    def pop(self, index):
        self._items.pop(index)
        for observer in self.observers:
            observer.observe_pop(self, index)

    def remove(self, item):
        self.pop(self.index(item))

    def append(self, item):
        self.insert(len(self), item)

from proxyclass import proxy_class
List = proxy_class(List, '_items', methods=[
    '__getitem__',
    '__len__',
    'index',
])
