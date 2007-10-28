# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from lib.observer import Observable

class CacheMap(object):
    def __init__(self, func, l, with_index=False):
        self.obs_list = Observable()
        self.with_index = with_index
        self.func = func
        self._list = l
        
        src = self._list
        if with_index:
            src = enumerate(src)
        self._cache = map(self.func, src)
        
        l.obs_list.add_observer(self, '_list_')

    def _list_insert(self, index, item):
        if self.with_index:
            new_item = self.func((index, item))
        else:
            new_item = self.func(item)
        self._cache.insert(index, new_item)
        self.obs_list.notify.insert(index, new_item)

    def _list_pop(self, index, value):
        result = self._cache.pop(index)
        self.obs_list.notify.pop(index, result)

    def _list_replace(self, index, old_value, new_value):
        if self.with_index:
            new_item = self.func((index, new_value))
        else:
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
