from observer import Observable, observed_method

class CacheMap(Observable):
    def __init__(self, func, l):
        Observable.__init__(self)
        self.func = func
        self._list = l
        self._cache = map(self.func, self._list)

    def observe_insert(self, index, item):
        self._cache.insert(index, self.func(item))

    def observe_pop(self, index):
        # TODO: Should call destroy() here
        self._cache.pop(index)

from proxyclass import proxy_class
CacheMap = proxy_class(CacheMap, '_cache', methods=[
    '__getitem__',
    '__len__',
    'index',
])
