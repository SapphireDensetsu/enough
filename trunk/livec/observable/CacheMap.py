from observer import Observable
from List import ListObserver

class CacheMap(Observable, ListObserver):
    def __init__(self, func, l):
        Observable.__init__(self)
        self.func = func
        self._list = l
        self._cache = map(self.func, self._list)
        l.add_observer(self)

    def observe_insert(self, list, index, item):
        new_item = self.func(item)
        self._cache.insert(index, new_item)
        for observer in self.observers:
            observer.observe_insert(self, index, new_item)

    def observe_pop(self, list, index):
        # TODO: Should call destroy() here?
        result = self._cache.pop(index)
        for observer in self.observers:
            observer.observe_pop(self, index)
        return result

from proxyclass import proxy_class
CacheMap = proxy_class(CacheMap, '_cache', methods=[
    '__getitem__',
    '__len__',
    'index',
])
