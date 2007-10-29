# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from lib.observer import Observable

class CacheMap(object):
    def __init__(self, func, l):
        self.obs_list = Observable()
        self.func = func
        self._list = l
        
        self._cache = map(self.func, self._list)
        
        l.obs_list.add_observer(self, '_list_')

    def _list_insert(self, index, item):
        new_item = self.func(item)
        self._cache.insert(index, new_item)
        self.obs_list.notify.insert(index, new_item)

    def _list_pop(self, index, value):
        result = self._cache.pop(index)
        self.obs_list.notify.pop(index, result)

    def _list_replace(self, index, old_value, new_value):
        new_item = self.func(new_value)
        old_item = self._cache[index]
        self._cache[index] = new_item
        self.obs_list.notify.replace(index, old_item, new_item)

from lib.proxyclass import proxy_class
CacheMap = proxy_class(CacheMap, '_cache', methods=[
    '__getitem__',
    '__len__',
    'index',
])
