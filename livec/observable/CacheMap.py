from observer import Observable

class CacheMap(object):
    def __init__(self, func, l):
        self.obs = Observable()
        self.func = func
        self._list = l
        self._cache = map(self.func, self._list)
        l.obs.add_observer(self, 'observe_')

    def observe_insert(self, index, item):
        new_item = self.func(item)
        self._cache.insert(index, new_item)
        self.obs.insert(index, new_item)

    def observe_pop(self, index):
        # TODO: Should call destroy() here?
        result = self._cache.pop(index)
        self.obs.pop(index)
        return result

from proxyclass import proxy_class
CacheMap = proxy_class(CacheMap, '_cache', methods=[
    '__getitem__',
    '__len__',
    'index',
])
