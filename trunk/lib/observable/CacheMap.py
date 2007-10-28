# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from lib.observer import Observable

class CacheMap(object):
    def __init__(self, func, l):
        self.obs_list = Observable()
        self.func = func
        self._list = l
        self._cache = map(self.func, self._list)
        l.obs_list.add_observer(self, 'observe_')

    def observe_insert(self, index, item):
        new_item = self.func(item)
        self._cache.insert(index, new_item)
        self.obs_list.notify.insert(index, new_item)

    def observe_pop(self, index, value):
        # TODO: Should call destroy() here?
        result = self._cache.pop(index)
        self.obs_list.notify.pop(index, result)

from lib.proxyclass import proxy_class
CacheMap = proxy_class(CacheMap, '_cache', methods=[
    '__getitem__',
    '__len__',
    'index',
])
